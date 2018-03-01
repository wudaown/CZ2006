package ss4.Control;

public class FollowManager {
    private static FollowManager singleInstance = new FollowManager();

    private FollowManager() {

    }
    public static FollowManager getInstance() {
        return singleInstance;
    }
}
