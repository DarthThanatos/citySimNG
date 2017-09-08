package py4jmediator;

import org.json.JSONObject;

public interface ViewModel {
	
	public MainMenuViewModel getMainMenuViewModel();
	public CreatorViewModel getCreatorViewModel(); 
	public GameMenuViewModel getGameMenuViewModel();
	
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
}
