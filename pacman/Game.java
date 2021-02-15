package pacman;

import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.paint.Color;
import javafx.scene.shape.Arc;
import javafx.scene.shape.ArcType;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.List;


public class Game extends Application {

   private final int mapSizeX = 280;
   private final int mapSizeY = 260;
   private final double speed = 0.009;
   private Pacman pacman;
   private final Rectangle mainRectangle = new Rectangle(0, 0, mapSizeX, mapSizeY);

    @Override
    public void start(Stage stage) throws Exception {


        Group root = new Group();

        Scene scene = new Scene(root, mapSizeX, mapSizeY);
        scene.setFill(Color.DARKBLUE);

        pacman = new Pacman();
        root.getChildren().add(pacman.getSelf());


        // Map creation
        // {x, y, width, height}
        int[][] map = new int[][] {{20, 20, 20, 20}, {60, 20, 20, 60}, {100, 20, 80, 20},
                {200, 20, 20, 60}, {240, 20, 20, 20}, {20, 60, 40, 20}, {100, 60, 80, 20},
                {220, 60, 40, 20}, {20, 100, 20, 60}, {60, 100, 20, 60}, {100, 100, 20, 60},
                {120, 120, 40, 20}, {160, 100, 20, 60}, {200, 100, 20, 60}, {240, 100, 20, 60}};

        List<Rectangle> rectangles = new ArrayList<>();

//        Rectangle rec = new Rectangle(20, 20, 20, 20);
//        rec.setFill(Color.YELLOW);
//        root.getChildren().add(rec);

        for (int i=0; i<map.length; i++){

            Rectangle rectangle = new Rectangle(map[i][0], map[i][1], map[i][2], map[i][3]);

            rectangles.add(rectangle);
            root.getChildren().add(rectangle);
        }

        for (int i=0; i<8; i++){

            Rectangle rectangle = new Rectangle(map[i][0], 260 - map[i][1] - map[i][3], map[i][2], map[i][3]);

            rectangles.add(rectangle);
            root.getChildren().add(rectangle);
        }


        scene.addEventHandler(KeyEvent.KEY_PRESSED,
                new EventHandler<KeyEvent>() {
                    @Override
                    public void handle(KeyEvent keyEvent) {
                        if (keyEvent.getCode() == KeyCode.LEFT){
                            pacman.setDirection(Direction.LEFT);
//                            System.out.println(pacman.getSelf().getCenterX());
                        }
                        if (keyEvent.getCode() == KeyCode.RIGHT){
                            pacman.setDirection(Direction.RIGHT);
                        }
                        if (keyEvent.getCode() == KeyCode.UP){
                            pacman.setDirection(Direction.UP);
                        }
                        if (keyEvent.getCode() == KeyCode.DOWN){
                            pacman.setDirection(Direction.DOWN);
                        }

                        for (Rectangle rectangle : rectangles){
                            if (rectangle.contains(pacman.getFrontPoint())){
                                return;
                            }
                            if (rectangle.contains(pacman.getSidePoints()[0])){
                                return;
                            }
                            if (rectangle.contains(pacman.getSidePoints()[1])){
                                return;
                            }

                        }

                        if (!mainRectangle.contains(pacman.getFrontPoint())){
                            return;
                        }
                        if (!mainRectangle.contains(pacman.getSidePoints()[0])){
                            return;
                        }
                        if (!mainRectangle.contains(pacman.getSidePoints()[1])){
                            return;
                        }

                        pacman.Move();

                    }
                }
        );


        stage.setTitle("Pacman");
        stage.setScene(scene);
        stage.show();



    }



}
