package py4jmediator;

import java.util.Set;

import org.json.JSONObject;

public interface ViewModel {
	
	public MainMenuViewModel getMainMenuViewModel();
	public CreatorViewModel getCreatorViewModel(); 
	public GameMenuViewModel getGameMenuViewModel();
	public LoaderViewModel getLoaderViewModel ();
	
	public interface MainMenuViewModel{
		public void displayMainMenu();
	}
	
	public interface GameMenuViewModel{
		public void displayGameMenu();
	}
	
	public interface CreatorViewModel{
		public void displayCreator();
		public void displayDependenciesGraph(JSONObject jsonGraph);
		public void displayMsg(String errorMsg);
	}
	
	public interface LoaderViewModel{
		public void displayLoader();
		public void displayDependenciesGraph(JSONObject graphDesc);
		public void displayPossibleDependenciesSets(Set<String> possibleSets);
	}
}
