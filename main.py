from datetime import datetime
import pickle

class Event:
    """Event class definition"""
    def __init__(self, title, date, description=""):
        """Initialization method"""
        self.title = title  # Define title
        self.date = date  # Define date
        self.description = description  # Define description
        dateArray = [int(i) for i in date.split("-")]
        self.year = dateArray[0]
        self.month = dateArray[1]
        self.day = dateArray[2]

    def __lt__(self, other):
        """
        Method to compare sizes
        """
        if self.title == other.title:
            return False
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        if self.day != other.day:
            return self.day < other.day

    def __eq__(self, other):
        return self.title == other.title

    def __gt__(self, other):
        if self.title == other.title:
            return False
        if self.year != other.year:
            return self.year > other.year
        if self.month != other.month:
            return self.month > other.month
        if self.day != other.day:
            return self.day > other.day

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None
    def insert(self, key):
        self.root = self.insert_travel(self.root, key)

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def insert_travel(self, root, key):
        if root is None:
            root = AVLNode(key)
            return root
        if key == root.key:
            root.key = key
            return root
        if key < root.key:
            root.left = self.insert_travel(root.left, key)
        else:
            root.right = self.insert_travel(root.right, key)
        self.update_height(root)
        if self.get_balance(root) > 1:
            if self.get_balance(root.left) >= 0:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        elif self.get_balance(root) < -1:
            if self.get_balance(root.right) <= 0:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)
        else:
            return root

    def remove(self, key):
        self.hasKey = False
        self.root = self.remove_travel(self.root, key)
        return self.hasKey

    def remove_travel(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self.remove_travel(root.left, key)
        elif key > root.key:
            root.right = self.remove_travel(root.right, key)
        else:
            self.hasKey = True
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            min_node = self.find_right_min(root)
            root.key = min_node.key
            root.right = self.remove_travel(root.right, root.key)

        self.update_height(root)
        if self.get_balance(root) > 1:
            if self.get_balance(root.left) >= 0:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        elif self.get_balance(root) < -1:
            if self.get_balance(root.right) <= 0:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)
        else:
            return root

    def find_right_min(self, root):
        right = root.right
        while right.left is not None:
            right = right.left
        return right

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        if node is None:
            return
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

    def left_rotate(self, root):
        newRoot = root.right
        left = newRoot.left
        newRoot.left = root
        root.right = left
        self.update_height(root)
        self.update_height(newRoot)
        return newRoot

    def right_rotate(self, root):
        newRoot = root.left
        right = newRoot.right
        newRoot.right = root
        root.left = right
        self.update_height(root)
        self.update_height(newRoot)
        return newRoot

    def Inorder(self):
        self.inorderList = []
        self.inorder_travel(self.root)
        return self.inorderList.copy()

    def inorder_travel(self, root):
        if root is None:
            return
        self.inorder_travel(root.left)
        self.inorderList.append(root.key)
        self.inorder_travel(root.right)

class EventScheduler:
    """Event Scheduler class definition"""
    def __init__(self, storage_file='./events.json'):
        """Initialization method"""
        self.storage_file = storage_file  # Define the persistent file save path
        self.load_events()  # Load events persistently

    def add_event(self, title, date, description=""):
        """Method to add an event"""
        new_event = Event(title, date, description)  # Generate event object according to passed parameters
        self.events.insert(new_event)

    def remove_event(self, title):
        """Method to remove an event"""
        remove_event = Event(title, "1001-01-01", "")
        return self.events.remove(remove_event)

    def list_events(self):
        """Method to list events"""
        sorted_events = self.events.Inorder()
        if len(sorted_events) == 0:
            print("There are no events.")
        for event in sorted_events:
            print(f"Title: {event.title}, Date: {event.date}, Description: {event.description}")

    def load_events(self):
        """Load events method"""
        try:
            with open(self.storage_file, "rb") as file:
                self.events = pickle.load(file)
        except:
            self.events = AVL()

    def save_events(self):
        """Save events method"""
        with open(self.storage_file, 'wb') as file:
            pickle.dump(self.events, file)

def checkData(date):
    """Check if the date is in the correct format"""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

def main():
    """Main function"""
    scheduler = EventScheduler()
    try:
        while True:
            action = input("Select the action you want to take (add, remove, list, exit): ").lower()
            if action == "add":
                title = input("Title: ")
                date = input("Date (YYYY-MM-DD): ")
                description = input("Description: ")
                if not checkData(date):
                    print("The input date format is incorrect, adding failed")
                else:
                    scheduler.remove_event(title)
                    scheduler.add_event(title, date, description)
            elif action == "remove":
                title = input("Please enter the title of the event you want to remove: ")
                result = scheduler.remove_event(title)
                if not result:
                    print("Title not exists! Remove error.")
                else:
                    print("Remove successfully")
            elif action == "list":
                scheduler.list_events()
            elif action == "exit":
                scheduler.save_events()
                break
            else:
                print("Invalid operation. Please reselect.")
    except:
        scheduler.save_events()

if __name__ == "__main__":
    main()
