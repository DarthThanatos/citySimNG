package py4jmediator;
import py4j.*;

public class Presenter {

    private static GatewayServer gatewayServer;
    private static Presenter presenter;
    private static ViewModel viewModel;
    private static ClientServer clientServer;
    
    private static MainMenuPresenter mainMenuPresenter = new MainMenuPresenter();
    private static CreatorPresenter creatorPresenter = new CreatorPresenter(); 
    private static MapPresenter mapPresenter = new MapPresenter();
    private static LoaderPresenter loaderPresenter = new LoaderPresenter();
    private static GameMenuPresenter gameMenuPresenter = new GameMenuPresenter();

    public static void initViewModel(){
        // We get an entry point from the Python side
        clientServer = new ClientServer(null);
        viewModel = (ViewModel) clientServer.getPythonServerEntryPoint(new Class[] { ViewModel.class });
    }
    
    ViewModel getViewModel(){
    	return viewModel;
    }
    
    public static Presenter getInstance(){
    	if(presenter != null) return presenter;
    	
    	presenter = presenter == null ? new Presenter() : presenter;
    	gatewayServer = new GatewayServer(presenter,25335);
    	gatewayServer.start();	
    	return presenter;
    }
    
    public MainMenuPresenter getMainMenuPresenter(){
    	return mainMenuPresenter;
    }
    
    public CreatorPresenter getCreatorPresenter(){
    	return creatorPresenter;
    }

    public MapPresenter getMapPresenter() {
        return mapPresenter;
    }

    public GameMenuPresenter getGameMenuPresenter(){
    	return gameMenuPresenter;
    }

    public LoaderPresenter getLoaderPresenter(){
    	return loaderPresenter;
    }

    public static void cleanup(){
    	clientServer.shutdown();
    	gatewayServer.shutdown();
    }
}
