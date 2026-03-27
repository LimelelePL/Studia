object cw4 extends App{
    def sqrList (list : List[Int]) : List[Int] = { 
    if list.isEmpty then Nil
    else (list.head * list.head) :: sqrList(list.tail)
    }

    val sqrListFun: List[Int] => List[Int] = list =>
        if list.isEmpty then Nil
        else (list.head*list.head) :: sqrListFun(list.tail)

    
    val fefw = sqrList


    val square = sqrList(List(2,3,4))
    val t1 = sqrList(List())
    val t2 = sqrListFun(List(0,0,0,0,0))
}