import os
import torch
import numpy as np
import cv2
from torch.autograd import Variable
import torch.backends.cudnn as cudnn

try:
    from craft import CRAFT
    from craft_utils import (
        getDetBoxes,
        adjustResultCoordinates,
    )
    from utils import (
        copy_state_dict,
        fix_path,
    )
    from file_utils import save_result
    from imgproc import (
        load_image,
        resize_aspect_ratio,
        normalize_mean_variance,
        cvt2_heatmap_img
    )
except (ImportError, ModuleNotFoundError):
    from .craft import CRAFT
    from .craft_utils import (
        getDetBoxes,
        adjustResultCoordinates,
    )
    from .utils import (
        copy_state_dict,
        fix_path,
    )
    from .file_utils import save_result
    from .imgproc import (
        load_image,
        resize_aspect_ratio,
        normalize_mean_variance,
        cvt2_heatmap_img
    )


def test_net(
        net: torch.nn.Module,
        image: np.ndarray,
        text_threshold: float = 0.7,
        link_threshold: float = 0.4,
        low_text: float = 0.4,
        cuda: bool = False,
        poly: bool = False,
        canvas_size: int = 1280,
        mag_ratio: float = 1.5,
        refine_net: torch.nn.Module = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    # resize
    img_resized, target_ratio, size_heatmap = resize_aspect_ratio(
        image, canvas_size,
        interpolation=cv2.INTER_LINEAR,
        mag_ratio=mag_ratio
    )
    ratio_h = ratio_w = 1 / target_ratio

    # preprocessing
    x = normalize_mean_variance(img_resized)
    x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
    x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]
    if cuda:
        x = x.cuda()

    # forward pass
    with torch.no_grad():
        y, feature = net(x)

    # make score and link map
    score_text = y[0, :, :, 0].cpu().data.numpy()
    score_link = y[0, :, :, 1].cpu().data.numpy()

    # refine link
    if refine_net is not None:
        with torch.no_grad():
            y_refiner = refine_net(y, feature)
        score_link = y_refiner[0, :, :, 0].cpu().data.numpy()

    # Post-processing
    boxes, polys = getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)

    # coordinate adjustment
    boxes = adjustResultCoordinates(boxes, ratio_w, ratio_h)
    polys = adjustResultCoordinates(polys, ratio_w, ratio_h)
    for k in range(len(polys)):
        if polys[k] is None:
            polys[k] = boxes[k]

    # render results (optional)
    render_img = score_text.copy()
    render_img = np.hstack((render_img, score_link))
    ret_score_text = cvt2_heatmap_img(render_img)

    return boxes, polys, ret_score_text


class TNet:
    """
    Loads uop the testnet code.
    """
    bboxes = polys = score_text = None

    def __init__(
        self,
        cuda: bool = False,
        poly: bool = False,
        trained_model: str = '~/.cache/mcraft/craft_mlt_25k.pth',
        refiner_model: str = '~/.cache/mcraft/craft_refiner_CTW1500.pth',
        refine: bool = False,
    ):
        self.net = CRAFT()
        self.cuda = cuda
        self.poly = poly
        self.trained_model = fix_path(trained_model)
        self.refiner_model = fix_path(refiner_model)
        if self.cuda:
            self.net.load_state_dict(copy_state_dict(torch.load(self.trained_model)))
        else:
            self.net.load_state_dict(copy_state_dict(torch.load(self.trained_model, map_location='cpu')))

        if self.cuda:
            self.net = self.net.cuda()
            self.net = torch.nn.DataParallel(self.net)
            cudnn.benchmark = False

        self.net.eval()

        self.refine_net = None
        if refine:
            try:
                from refinenet import RefineNet
            except ImportError:
                from .refinenet import RefineNet
            self.refine_net = RefineNet()
            print('Loading weights of refiner from checkpoint (' + refiner_model + ')')
            if self.cuda:
                self.refine_net.load_state_dict(copy_state_dict(torch.load(self.refiner_model)))
                self.refine_net = self.refine_net.cuda()
                self.refine_net = torch.nn.DataParallel(self.refine_net)
            else:
                self.refine_net.load_state_dict(copy_state_dict(torch.load(self.refiner_model, map_location='cpu')))

            self.refine_net.eval()
            self.poly = True

    def reset(self):
        """
        Clear variables.
        """
        self.bboxes = self.polys = self.score_text = None
        return self

    def forward(
        self,
        image: np.ndarray,
        text_threshold: float = 0.7,
        link_threshold: float = 0.4,
        low_text: float = 0.4,
        mag_ratio: float = 1.5,
        canvas_size: int = 1280,

    ):
        """
        Forward pass.
        """
        self.reset()
        self.bboxes, self.polys, self.score_text = test_net(
            net=self.net,
            image=image,
            text_threshold=text_threshold,
            link_threshold=link_threshold,
            low_text=low_text,
            cuda=self.cuda,
            poly=self.poly,
            canvas_size=canvas_size,
            mag_ratio=mag_ratio,
            refine_net=self.refine_net
        )

        return self.bboxes, self.polys, self.score_text

    def test(
        self,
        image_path: str,
        text_threshold: float = 0.7,
        link_threshold: float = 0.4,
        low_text: float = 0.4,
        mag_ratio: float = 1.5,
        canvas_size: int = 1280,
    ):
        """
        This is a replication of the old test.py file.
        """
        image = load_image(image_path)
        bboxes, polys, score_text = self.forward(
            image=image,
            text_threshold=text_threshold,
            link_threshold=link_threshold,
            low_text=low_text,
            mag_ratio=mag_ratio,
            canvas_size=canvas_size
        )
        filename, file_ext = os.path.splitext(os.path.basename(image_path))
        mask_file = "res_" + filename + '_mask.jpg'
        cv2.imwrite(mask_file, score_text)
        save_result(image_path, image[:, :, ::-1], polys, dirname='')
