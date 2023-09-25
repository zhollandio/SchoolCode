/*
 * Model class 
 * hold an ArrayList of Tubes and a mario and scroll position 
 *
 */

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;


/*
 * model class
 */

public class Model {

	// array list of tubes
	ArrayList<Sprite> sprites;

	// tube comparator
	SpriteComparator spriteComparator = new SpriteComparator();
	
	// tubes
	ArrayList<Tube> tubes = new ArrayList<Tube>();
	
	// mario
	Mario mario;
	
	// brick
	ArrayList<Brick> bricks = new ArrayList<Brick>();
	

	int scrollPos = 0; // horizontal scroller

	// initialize model to hold an arrayList of tubes
	public Model() {
		// make aray list of tubes
		sprites = new ArrayList<Sprite>();

		// make default tube
		addTube(600, 300);

		// make mario
		mario = new Mario(500, 500);
		sprites.add(mario);
		
		
	}

	// return true if can go right
	public boolean marioCanGoRight() {
		// check for collission
		Iterator<Sprite> itr = sprites.iterator();

		while (itr.hasNext()) {
			Sprite s = itr.next();

			if (s!=mario && !mario.canGoRight(s.x-5, s.y, s.width, s.height)) {
				
				return false;
			}
		}

		return true;
	}

	// return true if can go left
	public boolean marioCanGoLeft() {
		// check for collission
		Iterator<Sprite> itr = sprites.iterator();

		while (itr.hasNext()) {
			Sprite s = itr.next();

			if (s!=mario && !mario.canGoLeft(s.x+5, s.y,s.width, s.height)) {
				return false;
			}
		}

		return true;
	}

	// return true if can go up
	public boolean marioCanGoUp() {
		// check for collission
		Iterator<Sprite> itr = sprites.iterator();

		while (itr.hasNext()) {
			Sprite s = itr.next();
            
    			if (s!=mario && !mario.canGoUp(s.x, s.y,s.width, s.height)) {

    			mario.y=500;	
    			mario.vert_vel=0;
				return false;
			}
		}

		return true;
	}

	// return true if can go down
	public boolean marioCanGoDown() {
		// check for collission
		Iterator<Sprite> itr = sprites.iterator();

		while (itr.hasNext()) {
			Sprite s = itr.next();

			if (s!=mario && !mario.canGoDown(s.x, s.y,s.width, s.height)) {
				return false;
			}
		}

		return true;
	}
	
	
	// return true if can go down
	public boolean marioIsClear() {
		// check for collission
		Iterator<Sprite> itr = sprites.iterator();

		while (itr.hasNext()) {
			Sprite s = itr.next();

			if (s!=mario && !mario.canGoDown(s.x, s.y-20,s.width, s.height)) {

				return false;
			}
		}

		return true;
	}
	
	
	// can move brick
	public boolean canMoveBricks()
	{
		for(Brick g:bricks)
		{

			for(Sprite s: sprites)
			{
				if(s instanceof Brick);
					
				else if(g.hasCollided(s.x,s.y,s.width,s.height))
					{
					    // change diretion
					    return false;
					}
			}
		}
		
		return true;
	}

	// update mario
	public void update() {

         // call update from each sprite
		for(Sprite s:sprites)
		{
			s.update();
		}
	}

	// add tube to model
	public void addTube(int x, int y) {
		Tube t = new Tube(x, y);

		// add tube to model
		sprites.add(t);
		tubes.add(t);

		// Whenever you add a new Tube to your model,
		// sort the ArrayList according to the horizontal positions of the
		// tubes.
		// using the tube comparator
		Collections.sort(sprites, spriteComparator);
	}
	
	
	
	// add 	brick to model
	public void addBrick(int x, int y) {
		Brick b = new Brick(x, y);

		// add tube to model
		sprites.add(b);
		bricks.add(b);


	}
	
	// remove tube at index
	public void removeSprite(int i) {
		if (i >= 0 && i < sprites.size())
			sprites.remove(i);
	}

	// remove tube
	public void removeSprite(Sprite s) {
		sprites.remove(s);
	}

	// find tube clicked on
	public 	Sprite hasClickedOnSprite(int x2, int y2) {
		for (Sprite s: sprites) {
			
			if(s != mario)
			{
			if (s.hasClickedOnSprite(x2, y2))
				return s;
			}
		}

		return null;
	}

	// first tube to show on screen
	int findFirstTubeOnScreen() {

		int size = sprites.size() - 1;

		int start = 0;
		int finish = size;

		while (true) {
			int mid = (start + finish) / 2;
			if (mid == start)
				return start;
			Sprite s = sprites.get(mid);
			if (s.x - scrollPos < -100)
				start = mid;
			else
				finish = mid;
		}

	}


}

// user to sort tubes
class SpriteComparator implements Comparator<Sprite> {
	public int compare(Sprite a, Sprite b) {
		if (a.x < b.x)
			return -1;
		else if (a.x > b.x)
			return 1;
		else
			return 0;
	}

	public boolean equals(Object obj) {
		return false;
	}
}
