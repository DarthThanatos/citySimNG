package py4jmediator;

import org.json.JSONObject;

public interface ViewModel {
	
	public MainMenuViewModel getMainMenuViewModel();
	public CreatorViewModel getCreatorViewModel(); 
	
	public interface MainMenuViewModel{
		public void displayMainMenu();
		public void displayLoader();
		public void displayCreator();
	}
	
	public interface CreatorViewModel{
		public void displayMainMenu();
		public void displayCreator();
		public void displayDependenciesGraph(JSONObject jsonGraph);
		public void displayMsg(String errorMsg);
	}
}
