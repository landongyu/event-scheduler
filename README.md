# Event Scheduler Application

This Event Scheduler is a command-line interface (CLI) application that allows users to add, remove, list, and exit the scheduling of events. It uses an AVL tree for efficient data management, ensuring that operations like insertion, deletion, and retrieval are performed optimally.

## Features

- **Add Event**: Users can add new events with a title, date, and description. If an event with the same title is added, it will replace the existing event.
- **Remove Event**: Users can remove events based on their title.
- **List Events**: Users can list all scheduled events in a sorted manner, ordered by date (which is Implemented by AVL tree).
- **Exit**: Users can exit the application.
- **Optional Description**: While adding an event, providing a description is optional.

## Why Use AVL Tree?

The AVL tree is a self-balancing binary search tree. In the context of this application, it offers several advantages:

- **Balanced Structure**: AVL trees maintain balance by ensuring that the height difference between the left and right subtrees of any node is at most 1. This balance guarantees O(log n) complexity for insertions, deletions, and lookups, where n is the number of events.
- **Efficient Operations**: With AVL trees, operations like adding, removing, and listing events are efficient, ensuring that the application remains responsive even as the number of events grows.
- **Sorted Data**: The AVL tree inherently maintains the events in a sorted order, which is beneficial for listing events chronologically.

## Complexity Analysis

Without using AVL or Red-Black trees, if we were to use a basic binary search tree (BST), the complexity could degrade to O(n) for operations like insertion, deletion, and lookup in the worst-case scenario (where the tree becomes a linked list). This would significantly impact performance, especially with a large number of events.

Similarly, using an unsorted array or linked list would result in O(n) complexity for insertion and deletion (in the worst case) and would require O(n log n) time to sort the events every time we need to list them.

In contrast, AVL trees ensure O(log n) complexity for insertion, deletion, and lookup operations, providing a significant performance advantage, particularly for applications with a large and dynamic dataset like an event scheduler.

## Exception Handling and Data Preservation

The application employs a try...except mechanism to handle unexpected terminations. User inputs are read in a loop, and in case of an abrupt closure or an input error, the application catches the exception. This triggers the immediate saving of the current state of events to a file, followed by a graceful termination of the program. This feature ensures that your event data is not lost, even if the program exits unexpectedly, providing additional reliability to the application's operation.

## Getting Started

To use the application, simply run `python main.py` and follow the CLI prompts to add, remove, list events, or exit the application.
