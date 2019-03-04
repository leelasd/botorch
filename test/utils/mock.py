#!/usr/bin/env python3

from collections import OrderedDict
from typing import List, Optional

import torch
from botorch.models import Model
from botorch.posteriors import Posterior
from torch import Tensor


EMPTY_SIZE = torch.Size()


class MockPosterior(Posterior):
    """Mock object that implements dummy methods and feeds through specified outputs"""

    def __init__(self, mean=None, variance=None, samples=None):
        self._mean = mean
        self._variance = variance
        self._samples = samples

    @property
    def device(self) -> torch.device:
        for t in (self._mean, self._variance, self._samples):
            if torch.is_tensor(t):
                return t.device
        return torch.device("cpu")

    @property
    def dtype(self) -> torch.dtype:
        for t in (self._mean, self._variance, self._samples):
            if torch.is_tensor(t):
                return t.dtype
        return torch.float32

    @property
    def event_shape(self) -> torch.Size:
        if self._samples is not None:
            return self._samples.shape
        return torch.Size()

    @property
    def mean(self):
        return self._mean

    @property
    def variance(self):
        return self._variance

    def rsample(
        self,
        sample_shape: Optional[torch.Size] = None,
        base_samples: Optional[Tensor] = None,
    ) -> Tensor:
        """Mock sample by repeating self._samples."""
        if base_samples is not None:
            raise RuntimeError("base_samples are not supported in MockPosterior")
        if sample_shape is None:
            sample_shape = torch.Size()
        return self._samples.expand(sample_shape + self._samples.shape)


class MockModel(Model):
    """Mock object that implements dummy methods and feeds through specified outputs"""

    def __init__(self, posterior: MockPosterior):
        self._posterior = posterior

    def posterior(
        self,
        X: Tensor,
        output_indices: Optional[List[int]] = None,
        observation_noise: bool = False,
    ) -> MockPosterior:
        return self._posterior

    def state_dict(self) -> None:
        pass

    def load_state_dict(
        self, state_dict: Optional[OrderedDict] = None, strict: bool = False
    ) -> None:
        pass
