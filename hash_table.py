from __future__ import annotations
from typing import Optional, Callable, Iterator


class Node:
    def __init__(self, key: str, value: int, next: Optional["Node"] = None) -> None:
        self.key = key
        self.value = value
        self.next = next


# ------------------------------------------------------------
# Hash functions 
# ------------------------------------------------------------

def hash_function1(table: "HashTable", key: str) -> int:
    return ord(key[0]) % table.size


def hash_function2(table: "HashTable", key: str) -> int:
    '''
    Task 2
    Improved hash function that reduces collisions.
    Uses polynomial rolling hash (djb2 style) to distribute keys more evenly.
    '''
    hash_val = 0
    for ch in key:
        hash_val = (hash_val * 31 + ord(ch)) % table.size
    return hash_val


# ------------------------------------------------------------
# Hash Table Class
# ------------------------------------------------------------

class HashTable:
    def __init__(self, size: int) -> None:
        self.size = size
        self.total = 0
        self.buckets: list[Optional[Node]] = [None] * size

    # --------------------------------------------------------
    # Core operations
    # --------------------------------------------------------

    def add(self, key: str, value: int, hf: Callable[["HashTable", str], int]) -> None:
        index = hf(self, key)
        head = self.buckets[index]

        # Replace existing key
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # Insert new node at head
        new_node = Node(key, value, head)
        self.buckets[index] = new_node
        self.total += 1

    def remove(self, key: str, hf: Callable[["HashTable", str], int]) -> bool:
        ''' 
        Task 3
        Remove key/value pair from hash table. Handles head, middle, and tail removal.
        Returns True if found and removed, False otherwise.
        '''
        index = hf(self, key)
        current = self.buckets[index]
        prev = None

        # Traverse the linked list in the bucket
        while current:
            if current.key == key:
                # Found the key
                if prev is None:
                    # Removing the head
                    self.buckets[index] = current.next
                else:
                    # Removing middle or tail
                    prev.next = current.next
                self.total -= 1
                return True
            prev = current
            current = current.next

        # Key not found
        return False

    def get(self, key: str, hf: Callable[["HashTable", str], int]) -> Optional[int]:
        index = hf(self, key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    # --------------------------------------------------------
    # dunder methods for easy interface
    # --------------------------------------------------------

    def __setitem__(self, key: str, value: int) -> None:
        self.add(key, value, hash_function1)

    def __getitem__(self, key: str) -> int:
        value = self.get(key, hash_function1)
        if value is None:
            raise KeyError(key)
        return value

    def __delitem__(self, key: str) -> None:
        if not self.remove(key, hash_function1):
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return self.get(key, hash_function1) is not None

    def __iter__(self) -> Iterator[str]:
        for bucket in self.buckets:
            current = bucket
            while current:
                yield current.key
                current = current.next

    # --------------------------------------------------------
    # Utility methods
    # --------------------------------------------------------

    def reset(self) -> None:
        self.buckets = [None] * self.size
        self.total = 0

    def collisions(self) -> int:
        '''
        Task 1
        Counts collisions in the hash table.
        A collision occurs when more than one key hashes to the same bucket.
        For each bucket, if the chain length is L, it contributes (L - 1) collisions.
        '''
        num = 0
        for bucket in self.buckets:
            count = 0
            current = bucket
            while current:
                count += 1
                current = current.next
            if count > 1:
                num += count - 1
        return num

    def display(self) -> None:
        # print out the hash table in a readable format.
        # best not alter the display function as it is used in evaluating the output.
        print(f"HashTable(size={self.size}, total={self.total})")
        for i, bucket in enumerate(self.buckets):
            print(f"bucket[{i}]", end="")
            current = bucket
            if not current:
                print(" -|")
                continue
            while current:
                print(f" -> (key={current.key}, value={current.value})", end="")
                current = current.next
            print(" -|")
        print()
