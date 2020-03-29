import torch
import torch.nn as nn
import torchvision.models as models

class Identity(nn.Module):
    def __init__(self):
        super(Identity, self).__init__()

    def forward(self, x):
        return x


class Lahacks_pre_module(nn.Module):
    def __init__(self):
        super(Lahacks_pre_module, self).__init__()

        self.model = models.wide_resnet50_2(pretrained=True)
        self.model.eval()
        self.model.fc = Identity()

    def forward(self, x):
        return self.model(x)


class Lahacks_module(nn.Module):
    def __init__(self, in_dim, out_dim):
        super(Lahacks_module, self).__init__()

        self.layer = nn.Sequential(nn.Linear(in_dim, 1024),
                                   nn.ReLU(),
                                   nn.Linear(1024, out_dim),
                                   nn.LogSoftmax(dim=1))

    def forward(self, x):
        return self.layer(x)


pre_model = Lahacks_pre_module()
model = Lahacks_module(2048, 6)
if torch.cuda.is_available():
    model.load_state_dict(torch.load('static/lahack_model2_15.pth'))
else:
    model.load_state_dict(torch.load('static/lahack_model2_15.pth', map_location=torch.device('cpu')))
model.eval()

if torch.cuda.is_available():
    pre_model.cuda()
    model.cuda()


def load_module():
    return pre_model, model