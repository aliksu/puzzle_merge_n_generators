"""
Copyright 2022 Alexey Yudin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Iterator, Any
import random


def merge(*generators: Iterator[Any]) -> Iterator[Any]:
    """Merge sorted generators into one."""
    generators_with_values = {}
    for generator in generators:
        try:
            generators_with_values[generator] = next(generator)
        except StopIteration:
            pass

    left_generators = len(generators)

    while left_generators:
        for generator, value in sorted(generators_with_values.items(), key=lambda x: x[1]):
            yield value

            try:
                generators_with_values[generator] = next(generator)
            except StopIteration:
                generators_with_values.pop(generator, None)
                left_generators -= 1

            break


if __name__ == "__main__":
    list_of_generators = []

    for _ in range(100):
        list_of_values = sorted([random.randint(random.randint(0, 300), 500) for _ in range(300)])
        list_of_generators.append(iter(list_of_values))

    result = merge(*list_of_generators)

    print(list(result))
