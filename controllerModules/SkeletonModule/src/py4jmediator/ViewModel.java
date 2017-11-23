package py4jmediator;

import entities.Building;
import entities.Dweller;
import entities.Resource;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.json.JSONObject;

public interface ViewModel {

	public MainMenuViewModel getMainMenuViewModel();
	public CreatorViewModel getCreatorViewModel();
	public GameMenuViewModel getGameMenuViewModel();
	public LoaderViewModel getLoaderViewModel ();
	public MapViewModel getMapViewModel();
	public TutorialViewModel getTutorialViewModel();

	public interface MapViewModel{
		public void displayMap();
		public void init(List<Resource> resources, List<Building> domesticBuildings,
						 List<Building> industrialBuildings, List<Dweller> dwellers,
						 String texture_one, String texture_two, String panelTexture, String mp3,
						 Map<String, Integer> initialResourcesValues,
						 Map<String, Integer> initialResourcesIncomes,
						 Map<String, Integer> actualResourcesConsumption,
						 Map<String, Integer> resourcesBalance, int availableDwellers);
		public void updateValuesForCycle(Map<String, Integer> actualResourcesValues,
										 Map<String, Integer> actualResourcesIncomes,
										 Map<String, Integer> actualResourcesConsumption,
										 Map<String, Integer> resourcesBalance,
										 Integer neededDwellers,
										 Integer availableDwellers);
		public void sendTutorialHints(String hints);
		public void resumeGame();
	}

	public interface MainMenuViewModel{
		public void displayMainMenu();
	}

	public interface GameMenuViewModel{
		public void displayGameMenu();
		public void animateCurrentPrices(HashMap<String, Integer> currentPrices);
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

	public interface TutorialViewModel {
		public void displayTutorial();
		public void displayTutorialPage(JSONObject jsonPage);
		public void displayDependenciesGraph(JSONObject jsonGraph);
		public void fetchTutorialIndex(String[] index);
		public void fetchNodes(List<String> buildingsList, 
		List<String> resourcesList, List<String> dwellersList );
	}
}