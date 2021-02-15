package pacman;

import javafx.geometry.Point2D;
import javafx.scene.paint.Color;
import javafx.scene.shape.Arc;
import javafx.scene.shape.ArcType;

import java.awt.*;

public class Pacman {

    private Arc self;
    private Direction direction;
    private final double speed = 5;
    private Point2D frontPoint;
    private Point2D[] sidePoints;
    private final double radius = 10.0;


    public Pacman(){
        self = new Arc();
        self.setCenterX(10);
        self.setCenterY(10);
        self.setRadiusX(radius);
        self.setRadiusY(radius);
        self.setStartAngle(45);
        self.setLength(360);
        self.setType(ArcType.ROUND);
        self.setFill(Color.YELLOW);
    }

    public Arc getSelf(){
        return self;
    }

    public void setDirection(Direction newDirection){
        direction = newDirection;

        double x = self.getCenterX();
        double y = self.getCenterY();
        double x1 = 0.0;
        double y1 = 0.0;
        double d = (1 - Math.sqrt(2)/2)*radius;

        if (direction == Direction.UP){
            y -= radius;
            // to avoid late check
            y -= 2;

            x1 = x;
            y1 = y - d;
            Point2D point1 = new Point2D(x1 + radius - d, y1);
            Point2D point2 = new Point2D(x1 - radius + d, y1);
            sidePoints = new Point2D[] {point1, point2};
        }
        if (direction == Direction.DOWN){
            y += radius;
            y += 2;
            x1 = x;
            y1 = y + d;
            Point2D point1 = new Point2D(x1 + radius - d, y1);
            Point2D point2 = new Point2D(x1 - radius + d, y1);
            sidePoints = new Point2D[] {point1, point2};
        }
        if (direction == Direction.RIGHT){
            x += radius;
            x += 3;
            x1 = x - d;
            y1 = y;
            Point2D point1 = new Point2D(x1, y1 + radius - d);
            Point2D point2 = new Point2D(x1, y1 - radius + d);
            sidePoints = new Point2D[] {point1, point2};
        }
        if (direction == Direction.LEFT){
            x -= radius;
            x -= 3;
            x1 = x + d;
            y1 = y;
            Point2D point1 = new Point2D(x1, y1 + radius - d);
            Point2D point2 = new Point2D(x1, y1 - radius + d);
            sidePoints = new Point2D[] {point1, point2};
        }

        frontPoint = new Point2D(x, y);

    }

    public Direction getDirection(){
        return direction;
    }

    public void Move(){

        if (direction == Direction.UP){
            self.setCenterY(self.getCenterY() - speed);
        }
        if (direction == Direction.DOWN){
            self.setCenterY(self.getCenterY() + speed);
        }
        if (direction == Direction.LEFT){
            self.setCenterX(self.getCenterX() - speed);
        }
        if (direction == Direction.RIGHT){
            self.setCenterX(self.getCenterX() + speed);
        }
    }

    public Point2D getFrontPoint(){
        return frontPoint;
    }

    public Point2D[] getSidePoints(){
        return sidePoints;
    }
}
