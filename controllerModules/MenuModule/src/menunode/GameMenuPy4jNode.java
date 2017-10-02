package menunode;

import com.google.common.eventbus.Subscribe;
import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Py4JNode;
import model.ExchangeCurrentPricesEvent;
import py4jmediator.*;
import utils.CollectionConcatenationUtils;

public class GameMenuPy4jNode extends Py4JNode implements GameMenuPresenter.OnGameMenuPresenterCalled{

	public GameMenuPy4jNode(DependenciesRepresenter dr,
			DispatchCenter dispatchCenter, String nodeName) {
		super(dr, dispatchCenter, nodeName);
	}


	@Subscribe
	public void onCurrentPricesEvent(ExchangeCurrentPricesEvent exchangeCurrentPricesEvent){
		//TODO - current prices visualization on such event receipt
		System.out.println("Game menu module got current prices: " + CollectionConcatenationUtils.mapToString(exchangeCurrentPricesEvent.getCurrentPrices()));
	}

	@Override
	public void atUnload() {
		super.atUnload();
	}


	private void unregisterEvBus(){
		try{
			dispatchCenter.getEventBus().unregister(this);
		}catch(Exception e) {

		}
	}

	private void registerEvBus(){
		try {
			dispatchCenter.getEventBus().register(this);
		}
		catch(Exception e){

		}

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
		registerEvBus();
		
	}
	
	@Override
	protected void atExit() {
		unregisterEvBus();
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
