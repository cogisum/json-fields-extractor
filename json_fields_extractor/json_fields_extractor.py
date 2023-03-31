import re
from collections import OrderedDict


class JsonFieldsExtractor:
    idx_matcher = re.compile(r'_(\d+)$')
    idx_field = '$idx' # start from 0

    def __init__(self, field_paths, squeeze=True):
        self.field_paths = field_paths
        self.squeeze = squeeze

    def _select_sub_list(self, data, condition):
        if condition == '*':
            return data
        results = []
        if isinstance(condition, tuple):
            path, func = condition
            use_idx = path == self.idx_field
            if not use_idx and not isinstance(path, list):
                path = [path]
            for i, sub in enumerate(data):
                value = i if use_idx else self._get(sub, path)
                if func(value):
                    results.append(sub)
        elif obj := self.idx_matcher.match(condition):
            idx = int(obj.group(1))
            results.append(data[idx])
        return results

    def _get(self, data, path):
        if data is None or not path:
            return data
        component = path[0]
        path = path[1:]
        results = None
        if isinstance(data, list):
            data = self._select_sub_list(data, component)
            results = [self._get(sub, path) for sub in data]
            if len(results) == 1 and self.squeeze:
                results = results[0]
        else:
            data = data.get(component)
            results = self._get(data, path)
        return results

    def __call__(self, data):
        results = OrderedDict()
        for field, path in self.field_paths.items():
            results[field] = self._get(data, path)
        return results
