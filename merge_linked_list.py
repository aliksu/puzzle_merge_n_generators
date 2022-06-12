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
from typing import Any, Iterator
import random


class ListNode:  # pylint: disable=too-few-public-methods
    """A node for a linked list."""
    def __init__(self, generator: Iterator[Any]) -> None:
        try:
            self.generator, self.value = generator, next(generator)
        except StopIteration:
            return

        self.next = None


class LinkedList:
    """Linked list."""
    def __init__(self, head: Any | None = None):
        self.head = head

    def insert(self, node: ListNode) -> None:
        """Add a list node to a linked list."""
        if self.head is None:
            self.head = node

            return

        current_node = self.head
        previous_node = None

        while current_node is not None:
            if current_node.value >= node.value:
                node.next = current_node

                if previous_node is None:
                    node.next = self.head
                    self.head = node
                else:
                    previous_node.next = node

                return

            previous_node, current_node = current_node, current_node.next

        previous_node.next = node


    def pop(self) -> ListNode:
        """Remove a first list node from a linked list."""
        if self.head is None:
            return None

        if self.head.next is None:
            node = self.head
            self.head = None
            node.next = None

            return node

        node = self.head
        self.head = node.next
        node.next = None

        return node


def merge(*generators: Iterator[Any]) -> Iterator[Any]:
    """Merge sorted generators into one."""
    left_generators = len(generators)
    generators_llist = LinkedList()

    for generator in generators:
        generators_llist.insert(ListNode(generator=generator))

    while left_generators:
        generator_node = generators_llist.pop()
        yield generator_node.value

        try:
            generators_llist.insert(ListNode(generator=generator_node.generator))
        except StopIteration:
            left_generators -= 1


if __name__ == "__main__":
    list_of_generators = []

    for _ in range(100):
        list_of_values = sorted([random.randint(random.randint(0, 300), 500) for _ in range(300)])
        list_of_generators.append(iter(list_of_values))

    result = merge(*list_of_generators)

    print(list(result))
