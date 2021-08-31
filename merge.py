def merge_slow(*generators):
    generators_with_values = {generator: next(generator) for generator in generators}
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


class LinkedList:
    def __init__(self, head=None):
        self.head = None

    def insert(self, node):
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

            previous_node = current_node
            current_node = current_node.next

        previous_node.next = node


    def pop(self):
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

    def print(self):
        node = self.head

        while node is not None:
            node = node.next


class GeneratorNode:
    def __init__(self, generator):
        self.generator = generator
        self.value = next(self.generator)
        self.next = None


def merge_faster(*generators):
    left_generators = len(generators)
    generators_llist = LinkedList()

    for generator in generators:
        generators_llist.insert(GeneratorNode(generator))

    while left_generators:
        generator_node = generators_llist.pop()
        yield generator_node.value

        try:
            generators_llist.insert(GeneratorNode(generator_node.generator))
        except StopIteration:
            left_generators -= 1


class GeneratorWithValue:
    def __init__(self, generator):
        self.generator = generator
        self.value = next(self.generator)

    def __gt__(self, other):
        return self.value > other.value


def merge_faster_bisect(*generators):
    import bisect

    left_generators = len(generators)
    generators_with_values = sorted([GeneratorWithValue(generator) for generator in generators], reverse=True)

    while left_generators:
        generator_with_value = generators_with_values.pop()

        yield generator_with_value.value

        try:
            generator_with_value.value = next(generator_with_value.generator)
        except StopIteration:
            left_generators -= 1
        else:
            bisect.insort(generators_with_values, generator_with_value)


if __name__ == '__main__':
    import random

    generators = []

    for _ in range(100):
        list_of_values = sorted([random.randint(random.randint(0, 300), 500) for _ in range(300)])
        generators.append(iter(list_of_values))

    result = merge_faster_bisect(*generators)

    print([x for x in result])

