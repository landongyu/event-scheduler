import json
from datetime import datetime
import pickle

class Event:
    """Define Event class."""
    def __init__(self, title, date, description=""):
        """Initialization method."""
        self.title = title
        self.date = date
        self.description = description
        dateArray = [int(i) for i in date.split("-")]
        self.year = dateArray[0]
        self.month = dateArray[1]
        self.day = dateArray[2]

    def __lt__(self, other):
        return self.title < other.title

    def __eq__(self, other):
        return self.title == other.title

    def __gt__(self, other):
        return self.title > other.title

class AVLNode:
    """Node class for AVL tree."""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    """AVL tree class."""
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self.insert_travel(self.root, key)

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def insert_travel(self, root, key):
        if not root:
            return AVLNode(key)
        if key < root.key:
            root.left = self.insert_travel(root.left, key)
        else:
            root.right = self.insert_travel(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.balance_tree(root, key)

    def balance_tree(self, root, key):
        balance = self.get_balance(root)

        # Left Left
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def remove(self, key):
        self.hasKey = False
        self.root = self.remove_travel(self.root, key)
        return self.hasKey

    def remove_travel(self, root, key):
        if not root:
            return root

        if key < root.key:
            root.left = self.remove_travel(root.left, key)
        elif key > root.key:
            root.right = self.remove_travel(root.right, key)
        else:
            self.hasKey = True
            if not root.left or not root.right:
                root = root.left or root.right
            else:
                temp = self.getMinValueNode(root.right)
                root.key = temp.key
                root.right = self.remove_travel(root.right, root.key)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.balance_tree(root, key)

    def getMinValueNode(self, node):
        if node is None or node.left is None:
            return node
        return self.getMinValueNode(node.left)

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def Inorder(self):
        self.inorderList = []
        self.inorder_travel(self.root)
        return self.inorderList

    def inorder_travel(self, root):
        if not root:
            return
        self.inorder_travel(root.left)
        self.inorderList.append(root.key)
        self.inorder_travel(root.right)

class EventScheduler:
    """Event scheduler class."""
    def __init__(self, storage_file='./events.pkl'):
        self.storage_file = storage_file
        self.load_events()

    def add_event(self, title, date, description=""):
        new_event = Event(title, date, description)
        self.events.insert(new_event)
        self.save_events()

    def remove_event(self, title):
        remove_event = Event(title, "2000-01-01")
        if not self.events.remove(remove_event):
            print("Event not found. Removal failed.")
        else:
            print("Event removed successfully.")
        self.save_events()

    def list_events(self):
        sorted_events = self.events.Inorder()
        if not sorted_events:
            print("There are no events.")
        else:
            for event in sorted_events:
                print(f"Title: {event.title}, Date: {event.date}, Description: {event.description}")

    def load_events(self):
        try:
            with open(self.storage_file, "rb") as file:
                self.events = pickle.load(file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            self.events = AVL()

    def save_events(self):
        with open(self.storage_file, 'wb') as file:
            pickle.dump(self.events, file)

def check_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def main():
    scheduler = EventScheduler()
    while True:
        action = input("Choose an action (add, remove, list, exit): ").lower()
        if action == "add":
            title = input("Title: ")
            date = input("Date (YYYY-MM-DD): ")
            description = input("Description: ")
            if not check_date(date):
                print("The input date format is incorrect, adding failed.")
            else:
                scheduler.add_event(title, date, description)
        elif action == "remove":
            title = input("Enter the title of the event to remove: ")
            scheduler.remove_event(title)
        elif action == "list":
            scheduler.list_events()
        elif action == "exit":
            break
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()
