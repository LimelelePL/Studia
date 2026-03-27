public class Main {
    final static char blackSquare='■';

    public static void main(String[] args) {
        int[][]board = createBoard(20,20);
        printBoard(board);
        System.out.println();

        board[2][4] = 1;
        board[3][4] = 1;
        board[3][5] = 1;
        board[4][4] = 1;

        printBoard(updateBoard(board));
        System.out.println();
        printBoard(updateBoard(updateBoard(board)));

    }

    public static int[][] createBoard(int rows, int cols){
        int[][] board = new int[rows][cols];

        for (int i = 1; i < rows; i++){
            for (int j = 1; j < cols; j++){
                board[i][j] = 0;
            }
        }
        return board;
    }

    public static void printBoard(int[][] board){
        for (int i = 0; i < board.length; i++){
            System.out.print("\n");
            for (int j = 0; j < board[i].length; j++){
                if (board[i][j] == 0){
                    System.out.print(blackSquare + " ");
                } else {
                    System.out.print(board[i][j] + " ");
                }
            }
        }
    }

    public static int [][] updateBoard(int[][] board) {
        int[][] updatedBoard = createBoard(board.length, board.length);
        int rows = board.length - 1;
        int cols = board[0].length - 1;

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                int neighbours = calculateNeighbouts(board, i, j);

                if (board[i][j] == 1) {
                    if (neighbours == 2 || neighbours == 3) {
                        updatedBoard[i][j] = 1;
                    } else {
                        updatedBoard[i][j] = 0;
                    }
                } else { // Komórka martwa
                    if (neighbours == 3) {
                        updatedBoard[i][j] = 1; // Ożywa
                    }
                }
            }
        }
            return updatedBoard;
        }

        public static int calculateNeighbouts ( int[][] board, int x, int y){

            int count = 0;

            for (int i = -1; i <= 1; i++) {
                for (int j = -1; j <= 1; j++) {
                    if (x >= 1 && y >= 1) {
                        int dx = x + i;
                        int dy = y + j;

                        if (i == 0 && j == 0) {
                            continue;
                        }
                        if (board[dx][dy] == 1) {
                            count++;
                        }
                    }
                }
            }
            return count;
        }
    }