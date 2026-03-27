
def count [A] (f: A => Boolean, list: List[A]) : Int = {
    list match
        case head :: next => if f (head) then 1 + count(f, next) else count(f, next) 
        case Nil => 0
} 

def squaresOfEvens (xs: List[Int]) : List[Int] = {
    (xs.filter(x => x % 2 == 0) ).map(x => x*x)
}
val squares =  squaresOfEvens(List(1,2,3,4,5));;

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