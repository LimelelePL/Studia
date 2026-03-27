import scala.collection.immutable.Queue
sealed trait bt [+A]
case object Empty extends bt[Nothing]
case class Node[A] (value:A, left: bt[A], right: bt[A]) extends bt[A] 

sealed trait Graphs[A]
case class Graph[A](succ: A => List[A]) extends Graphs[A]  

object Cwiczenia4 extends App{
    
    //zadanie 3
    val tt = Node(1,Node(2,Node(4,Empty,Empty),Empty),Node(3,Node(5,Empty,Node(6,Empty,Empty)),Empty))
    
    def breathBt[A] (tree: bt[A]): List[A] = {
        def helper(visited: List[A], queue: List[bt[A]]): List[A]= {
            queue match
                case Nil => visited.reverse
                case Empty :: rest => helper(visited, rest)
                case Node(elem, left, right) :: rest => 
                    helper(elem :: visited, rest ::: List(left , right))
        }
        helper(List(), List(tree))
    }

    println(breathBt(tt).toString())

    //zadanie 4

    def inner[A] (tree: bt[A]) : Int = {
        def iter[A] (tree: bt[A], currentDepth: Int) : Int = {
            tree match
                case Empty => 0
                case Node(value, left, right) => 
                    currentDepth + iter(left, currentDepth+1) + iter(right, currentDepth+1)
        }
        iter(tree, 0)
    }
    println(inner(tt))

    
    def outter[A] (tree: bt[A]) : Int = { 
         def iter[A] (tree: bt[A], currentDepth: Int) : Int = {
            tree match
                case Empty => currentDepth 
                case Node(value, left, right) => iter(left, currentDepth+1) + iter(right, currentDepth+1)
         }
         iter(tree, 0)
    }
    println(outter(tt))

    //zadanie 5

    def dfs[A] (graph: Graph[A], elem:A) : List[A] = {
        def helper (visited : List[A], stack : List[A]): List[A] = {
            stack match
                case Nil => visited.reverse
                case head :: next =>
                     if(visited.contains(head)) then helper(visited, next)
                     else helper( head :: visited, graph.succ(head) ::: next)
        }
        helper(List(), List(elem))
    }
    val g = Graph((i: Int) => 
        i match
            case 0 => List(3)
            case 1 => List(0, 2, 4)
            case 2 => List(1)
            case 3 => Nil
            case 4 => List(0, 2)
            case n =>
                throw new Exception(s"Graph g: node $n doesn't exist"))


    println(dfs(g,1))
}
