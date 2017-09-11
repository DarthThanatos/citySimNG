package py4jmediator;

import entities.Building;
import entities.Resource;
import org.json.JSONObject;

import java.util.List;
import java.util.Map;

public interface ViewModel {
	
	public MainMenuViewModel getMainMenuViewModel();
	public CreatorViewModel getCreatorViewModel();
	public MapViewModel getMapViewModel();

	public interface MapViewModel{
		public void displayMap();
		public void init(List<Resource> resources, List<Building> buildings, String texture_one, String texture_two,
						 Map<String, Integer> initialResourcesValues, Map<String, Integer> initialResourcesIncomes);
		public void updateResourcesValues(Map<String, Integer> actualResourcesValues,
										  Map<String, Integer> actualResourcesIncomes);
	}
	
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
