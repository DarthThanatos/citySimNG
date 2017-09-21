package menunode;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Py4JNode;
import py4jmediator.*;

public class GameMenuPy4jNode extends Py4JNode implements GameMenuPresenter.OnGameMenuPresenterCalled{

	public GameMenuPy4jNode(DependenciesRepresenter dr,
			DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
	}

	@Override
	public void atUnload() {
		
	}

	@Override
	protected void onLoop() {

		
	}

	@Override
	protected void atStart() {
		GameMenuPresenter gameMenuPresenter = Presenter.getInstance().getGameMenuPresenter();
		gameMenuPresenter.setOnGameMenuPresenterCalled(this);
		gameMenuPresenter.displayGameMenu();
		System.out.println("atStart gamemenu");
		
	}
	
	@Override
	protected void atExit() {
		Presenter.getInstance().getGameMenuPresenter().setOnGameMenuPresenterCalled(null);
	}

	@Override
	public void onGoToNewGame() {
		moveTo("MapNode");
		
	}

	@Override
	public void onGoToLoader() {
		moveTo("LoaderNode");
	}

	@Override
	public void onGoToExchange() {
		moveTo("ExchangeNode");
	}

	@Override
	public void onGoToTutorial() {
		moveTo("TutorialNode");		
	}

	@Override
	public void onGoToRanking() {
		moveTo("RankingNode");
	}

}
