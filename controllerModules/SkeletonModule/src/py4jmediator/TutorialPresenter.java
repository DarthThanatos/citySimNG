package py4jmediator;

import org.json.JSONObject;
import java.util.List;

public class TutorialPresenter {
	
	private OnTutorialPresenterCalled onTutorialPresenterCalled;
	
	public void setOnTutorialPresenterCalled(OnTutorialPresenterCalled onTutorialPresenterCalled){
		this.onTutorialPresenterCalled = onTutorialPresenterCalled;
	}
	
	public void returnToMenu(){
		if(onTutorialPresenterCalled != null)
			onTutorialPresenterCalled.onReturnToMenu();
	}

	public void fetchPage(int pageNr){
		if(onTutorialPresenterCalled != null)
			onTutorialPresenterCalled.onFetchPage(pageNr);
	}
	
	public void displayTutorial(){
		Presenter.getInstance().getViewModel().getTutorialViewModel().displayTutorial();
	}
	
	public void displayTutorialPage(JSONObject jsonPage){
		Presenter.getInstance().getViewModel().getTutorialViewModel().displayTutorialPage(jsonPage);
	}

	public void displayDependenciesGraph(JSONObject jsonGraph){
		Presenter.getInstance().getViewModel().getTutorialViewModel().displayDependenciesGraph(jsonGraph);
	}

	public void fetchTutorialIndex(String[] index){
		Presenter.getInstance().getViewModel().getTutorialViewModel().fetchTutorialIndex(index);
	}

	public void fetchNodes(List<String> buildingsList, 
		List<String> resourcesList, List<String> dwellersList){
		Presenter.getInstance().getViewModel().getTutorialViewModel().fetchNodes(buildingsList,
			resourcesList, dwellersList);
	}
	
	
	public interface OnTutorialPresenterCalled{
		public void onReturnToMenu();
		public void onFetchPage(int pageNr);
	}
}
