
class Contact:
    '''
    Contact class to represent a contact with a name and number.

    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.

    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The Contact object associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    HashTable class to store contacts using separate chaining.

    Attributes:
        size (int): The size of the hash table.
        data (list): Array of linked lists for collision handling.

    Methods:
        hash_function(key): Converts a name into an array index.
        insert(key, value): Adds or updates a contact.
        search(key): Finds a contact by name.
        print_table(): Displays all contacts in the hash table.
    '''

    def __init__(self, size):
        if size <= 0:
            raise ValueError("Hash table size must be greater than zero.")

        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        # Convert each character to its ASCII/Unicode value.
        # Add the values and use modulo to find the array index.
        total = 0

        for character in key:
            total += ord(character)

        return total % self.size

    def insert(self, key, value):
        # Find the correct index for this contact.
        index = self.hash_function(key)

        # Create a contact object.
        new_contact = Contact(key, value)

        # If the index is empty, insert the first node.
        if self.data[index] is None:
            self.data[index] = Node(key, new_contact)
            return

        # Otherwise, traverse the linked list.
        current = self.data[index]

        while current is not None:
            # Update the phone number if the name already exists.
            if current.key == key:
                current.value.number = value
                return

            current = current.next

        # A collision occurred, so add a new node at the front.
        new_node = Node(key, new_contact)
        new_node.next = self.data[index]
        self.data[index] = new_node

    def search(self, key):
        # Find the bucket where the contact should be stored.
        index = self.hash_function(key)

        current = self.data[index]

        # Search through the linked list.
        while current is not None:
            if current.key == key:
                return current.value

            current = current.next

        # Contact was not found.
        return None

    def print_table(self):
        # Print every index and its stored contacts.
        for index in range(self.size):
            current = self.data[index]

            if current is None:
                print(f"Index {index}: Empty")
            else:
                contacts = []

                while current is not None:
                    contacts.append(str(current.value))
                    current = current.next

                print(f"Index {index}: " + " -> ".join(contacts))


# ============================================================
# TESTING THE CONTACT MANAGEMENT SYSTEM
# ============================================================

if __name__ == "__main__":

    print("========== CONTACT MANAGEMENT SYSTEM ==========")

    # Create a hash table with 10 positions.
    table = HashTable(10)

    # Test 1: Print an empty hash table.
    print("\nTEST 1: Empty Hash Table")
    table.print_table()

    # Test 2: Insert contacts.
    print("\nTEST 2: Inserting Contacts")

    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")

    table.print_table()

    # Test 3: Search for an existing contact.
    print("\nTEST 3: Searching for John")

    contact = table.search("John")
    print("Search result:", contact)

    assert contact is not None
    assert contact.number == "909-876-1234"

    # Test 4: Handle hash collisions.
    print("\nTEST 4: Testing Hash Collisions")

    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")

    print("Amy's hash index:", table.hash_function("Amy"))
    print("May's hash index:", table.hash_function("May"))

    table.print_table()

    # Both names should still be searchable.
    assert table.search("Amy").number == "111-222-3333"
    assert table.search("May").number == "222-333-1111"

    # Test 5: Update a duplicate contact.
    print("\nTEST 5: Updating a Duplicate Contact")

    table.insert("Rebecca", "999-444-9999")

    table.print_table()

    updated_contact = table.search("Rebecca")
    print("Updated Rebecca:", updated_contact)

    assert updated_contact.number == "999-444-9999"

    # Test 6: Search for a contact that does not exist.
    print("\nTEST 6: Searching for a Missing Contact")

    missing_contact = table.search("Chris")
    print("Search result:", missing_contact)

    assert missing_contact is None

    # Test 7: Update a contact within a collision chain.
    print("\nTEST 7: Updating a Contact in a Collision Chain")

    table.insert("Amy", "555-666-7777")

    print("Updated Amy:", table.search("Amy"))

    assert table.search("Amy").number == "555-666-7777"
    assert table.search("May").number == "222-333-1111"

    # Test 8: Test the Contact and Node classes.
    print("\nTEST 8: Testing Contact and Node Classes")

    contact_1 = Contact("Riley", "123-456-7890")
    node_1 = Node(contact_1.name, contact_1)

    print("Contact:", contact_1)
    print("Node key:", node_1.key)
    print("Node value:", node_1.value)
    print("Node next:", node_1.next)

    assert str(contact_1) == "Riley: 123-456-7890"
    assert node_1.key == "Riley"
    assert node_1.next is None

    print("\n========== ALL TESTS PASSED ==========")
