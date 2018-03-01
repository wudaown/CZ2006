package ss4.Control;

public class DisplayManager {
    private static DisplayManager singleInstance = new DisplayManager();

    private DisplayManager() {

    }
    public static DisplayManager getInstance() {
        return singleInstance;
    }

}
