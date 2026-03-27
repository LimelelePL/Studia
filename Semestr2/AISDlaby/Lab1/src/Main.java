import java.util.Random;

public class Main {
    final static char blackSquare='■';

    public static void main(String[] args){
        int[][] board= createBoard(10,10);
        board[2][1]=1;
        board[2][2]=1;
        board[2][3]=1;
        board[3][4]=1;


        printBoard(board);

    }

    public static int [][]createBoard(int rows, int cols){
        int [][]board = new int[rows][cols];
        for(int i = 0; i < rows; i++){
            for(int j = 0; j < cols; j++){
                board[i][j] = 0;
            }
        }
        return board;
    }

    public static void printBoard(int [][]board){
        for(int i = 0; i < board.length; i++){
            System.out.println();
            for(int j = 0; j < board[i].length; j++){
                if(board[i][j] == 0){
                    System.out.print(blackSquare + " ");
                }
            }
        }
    }

    public static int[][] updateBoard(int [][]board){
        int[][] newBoard = new int[board.length][board[0].length];

        for(int i = 0; i < board.length; i++){
            for(int j = 0; j < board[i].length; j++){
                int neighbours = calculateNeighbours(board, i,j);

                if(board[i][j] == 1){
                board[i][j] = (neighbours==2 || neighbours ==3 )? 1 : 0;
                }
                else {
                    board[i][j] = (neighbours==3) ? 1 : 3;
                }
            }
        }
        return newBoard;
    }

    public static int calculateNeighbours(int[][] board, int x, int y){
        int count=0;

        for(int i = -1; i <= 1; i++){
            for(int j = -1; j <= 1; j++){
                if(i == 0 && j == 0){
                 continue;
                }

                int nx= x + i;
                int ny = y + j;

                if(nx >= 0 && ny >= 0 && nx < board.length && ny < board[0].length){
                    count+=board[nx][ny];
                }
            }
        }
        return count;
    }
}