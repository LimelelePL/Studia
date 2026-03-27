sealed trait Tree[+A] 
case object Empty extends Tree[Nothing]
case class Node[+A](elem:A, left: Tree[A], right: Tree[A]) extends Tree[A]

object zadania5 extends App {
    def allNodes[A] (tree : Tree[A]) : List[A] = {
        tree match
            case Empty => List();
            case Node(elem, left, right) => elem :: allNodes(left) ::: allNodes (right)
    }


    def sumNodes (tree: Tree[Int]): Int = {
        tree match
            case Empty => 0
            case Node(elem, left, right) => elem + sumNodes(left) + sumNodes(right)
    }


    val tree = Node(1, Node(2, Node (3, Empty, Empty), Empty), Node(4, Empty, Empty))
    val tree1 = Node(1, Node(-2, Node (-3, Empty, Empty), Empty), Node(-4, Empty, Empty))
    val tree2 = Empty
    val tree3 = Node(0, Empty, Empty)

    println("test 1: ")
    println(allNodes(tree).toString())
    println(sumNodes(tree))

    println("test 2: ")
    println(allNodes(tree1).toString())
    println(sumNodes(tree1))

    println("test 3: ")
    println(allNodes(tree2).toString())
    println(sumNodes(tree2))

    println("test 4: ")
    println(allNodes(tree3).toString())
    println(sumNodes(tree3))
}
