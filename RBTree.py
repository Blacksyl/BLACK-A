import operator

class Node:
    def __init__(self, key, value, isred=True):
        self.key = key
        self.value = value
        self.IsRed = isred
        self.LeftChild = None
        self.RightChild = None
        self.Parent = None

class RBTree:
    def __init__(self):
        self.Length = 0
        self.Root = None

    def showtree(self):
        if not self.Root:
            print('树为空，无法展示！')
        self.showtreeoperation(self.Root)

    def showtreeoperation(self, node):
        if not node:
            return
        self.showtreeoperation(node.LeftChild)
        if node.IsRed:
            color = 'Red'
        else:
            color = 'Black'
        if node.Parent:
            log = str(node.key) + '--' + str(node.value) + '--' + color + '-->Parent: ' + str(node.Parent.value)
        else:
            log = str(node.key) + '--' + str(node.value) + '--' + color + '-->Parent: None'
        print(log)
        self.showtreeoperation(node.RightChild)

    def remove(self, key):
        if not key:
            print("key为空")
        current = self.Root
        while current:
            if key == current.key:
                node = current
                if current.LeftChild:
                    node = self.getmaxnode(current.LeftChild)
                elif current.RightChild:
                    node = self.getminnode(current.RightChild)
                current.key = node.key
                current.value = node.value
                self.delete(node)
                self.Length -= 1
                current = None
            elif key < current.key:
                current = current.LeftChild
            else:
                current = current.RightChild

    def delete(self, node):
        if node == self.Root:
            self.Root = None
            return
        parent = node.Parent
        child = (node.LeftChild if node.LeftChild else node.RightChild)
        if child:
            child.Parent = parent
        isleft = (node == parent.LeftChild)
        if isleft:
            parent.LeftChild = child
        else:
            parent.RightChild = child
        if node.IsRed:
            return
        if child and child.IsRed:
            child.IsRed = False
        else:
            node = child
            brother = (parent.RightChild if isleft else parent.LeftChild)
            if isleft:
                self.adjustleftmissedblack(node, parent, brother)
            else:
                self.adjustrightmissedblack(node, parent, brother)

    def adjustleftmissedblack(self, node, parent, brother):
        if brother and brother.IsRed:
            self.leftrotate(brother, parent)
            reversecolor(brother, parent)
            brother = parent.RightChild
        if brother:
            oppchild = brother.LeftChild
            child = brother.RightChild
        else:
            oppchild = None
            child = None
        if child and child.IsRed:
            self.leftrotatetoaddblack(child, brother, parent)
        elif oppchild and oppchild.IsRed:
            self.rightrotate(oppchild, brother)
            reversecolor(oppchild, brother)
            self.leftrotatetoaddblack(brother, oppchild,parent)
        else:
            if brother:
                brother.IsRed = True
            if parent.IsRed:
                parent.IsRed = False
            else:
                node = parent
                parent = node.Parent
                if parent:
                    brother = getbrothernode(node)
                    if node == parent.LeftChild:
                        self.adjustleftmissedblack(node, parent, brother)
                    else:
                        self.adjustrightmissedblack(node, parent, brother)

    def adjustrightmissedblack(self, node, parent, brother):
        if brother and brother.IsRed:
            self.rightrotate(brother, parent)
            reversecolor(brother, parent)
            brother = parent.LeftChild
        if brother:
            oppchild = brother.RightChild
            child = brother.LeftCild
        else:
            oppchild = None
            child = None
        if child and child.IsRed:
            self.rightrotatetoaddblack(child, brother, parent)
        elif oppchild and oppchild.IsRed:
            self.leftrotate(oppchild, brother)
            reversecolor(oppchild, brother)
            self.rightrotatetoaddblack(brother, oppchild, parent)
        else:
            if brother:
                brother.IsRed = True
            if parent.IsRed:
                parent.IsRed = False
            else:
                node = parent
                parent = node.Parent
                if parent:
                    brother = getbrothernode(node)
                    if node == parent.LeftChild:
                        self.adjustleftmissedblack(node, parent, brother)
                    else:
                        self.adjustleftmissedblack(node, parent, brother)

    def getminnode(self, current):
        if not current.LeftChild:
            return current
        return self.getminnode(current.LeftChild)

    def getmaxnode(self, current):
        if not current.RightChild:
            return current
        return self.getmaxnode(current.RightChild)

    def rightrotatetoaddblack(self, node, brother, parent):
        self.rightrotate(brother, parent)
        brother.IsRed = parent.IsRed
        parent.IsRed = node.IsRed = False

    def leftrotatetoaddblack(self, node, brother, parent):
        self.leftrotate(brother, parent)
        brother.IsRed = parent.IsRed
        parent.IsRed = node.IsRed = False

    def containsoperation(self, node, key):
        if not node:
            return False
        if operator.lt(node.key, key):
            return self.contains(node.RightChild, key)
        if operator.gt(node.key, key):
            return self.contains(node.LeftChild, key)
        return True

    def contains(self, key):
        if not key:
            print("key为空！")
        return self.containsoperation(self.Root, key)

    def insert(self, key, value):
        if not key:
            print('key为空！')
        if not value:
            print('value为空！')
        if not self.Root:
            self.Root = Node(key, value, False)
            self.Length += 1
            return
        newnode = Node(key, value)
        self.findposition(self.Root, newnode)
        if newnode.Parent:
            self.Length += 1
            self.adjustnewred(newnode)

    def adjustnewred(self, node):
        parent = node.Parent
        if not parent:
            node.IsRed = False
            return
        if not parent.IsRed:
            return
        # print(parent.key)
        uncle = getbrothernode(parent)
        # print(uncle.key)
        grand = parent.Parent
        if uncle and uncle.IsRed:
            uncle.IsRed = parent.IsRed = False
            # print('uncle: ' + str(uncle.IsRed) + str(uncle.key))
            # print('parent: ' + str(parent.IsRed) + str(parent.key))
            grand.IsRed = True
            # print('grand: ' + str(grand.IsRed))
            self.adjustnewred(grand)
        else:
            if parent == grand.LeftChild:
                self.rightrotatefornewnode(node, parent, grand)
            else:
                self.leftrotatefornewnode(node, parent, grand)

    def rightrotatefornewnode(self, node, parent, grand):
        if node == parent.RightChild:
            self.leftrotate(node, parent)
            parent = node
        self.rightrotate(parent, grand)
        reversecolor(parent, grand)

    def leftrotatefornewnode(self, node, parent, grand):
        if node == parent.LeftChild:
            self.rightrotate(node, parent)
            parent = node
        self.leftrotate(parent, grand)
        reversecolor(parent, grand)

    def leftrotate(self, node, parent):
        self.operationforbothrotation(node, parent)
        parent.RightChild = node.LeftChild
        if node.LeftChild:
            node.LeftChild.Parent = parent
        node.LeftChild = parent

    def rightrotate(self, node, parent):
        self.operationforbothrotation(node, parent)
        parent.LeftChild = node.RightChild
        if node.RightChild:
            node.RightChild.Parent = parent
        node.RightChild = parent

    def operationforbothrotation(self, node, parent):
        grand = parent.Parent
        node.Parent = grand
        parent.Parent = node
        if not grand:
            self.Root = node
        elif parent == grand.RightChild:
            grand.RightChild = node
        else:
            grand.LeftChild = node

    def findposition(self, current, node):
        if operator.gt(current.key, node.key):
            if not current.LeftChild:
                current.LeftChild = node
                node.Parent = current
            else:
                self.findposition(current.LeftChild, node)
        elif operator.lt(current.key, node.key):
            if not current.RightChild:
                current.RightChild = node
                node.Parent = current
            else:
                self.findposition(current.RightChild, node)
        else:
            current.value = node.value

def getbrothernode(node):
    parent = node.Parent
    if node == parent.LeftChild:
        return parent.RightChild
    else:
        return parent.LeftChild

def reversecolor(parent, grand):
    grand.IsRed = not grand.IsRed
    parent.IsRed = not parent.IsRed
    if not parent.Parent:
        parent.IsRed = False


if __name__ == '__main__':
    tree = RBTree()
    tree.insert(12, 12)
    tree.insert(9, 9)
    tree.insert(23, 23)
    tree.insert(45, 45)
    tree.insert(36, 36)
    tree.insert(77, 77)
    tree.insert(83, 83)
    tree.insert(66, 66)
    tree.insert(89, 89)
    tree.insert(16, 16)
    tree.remove(66)
    tree.remove(89)
    tree.remove(45)
    tree.remove(36)
    tree.showtree()
    print(tree.Length)

