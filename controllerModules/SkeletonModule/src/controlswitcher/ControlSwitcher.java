package controlswitcher;

import java.net.Socket;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

import constants.Consts;
import py4j.GatewayServer;
import py4jmediator.Presenter;
import controlnode.Node;
import monter.BaseMonter;
import monter.SystemMonter;

public class ControlSwitcher {

	private static final Logger logger = Logger.getLogger( ControlSwitcher.class.getName() );

	public static void main(String[] args)throws Exception{
		logger.setLevel(Consts.DEBUG_LEVEL);
		for(String arg: args) {
			if(arg.equals("--d") || arg.equals("--debug")) {
				GatewayServer.turnLoggingOn();
			}
		}
		Presenter.getInstance();
		checkIfViewReady();
		Node currentNode = mountGraph();
		mainLoop(currentNode);
		cleanup();
	}	

	
	private static void cleanup(){
		Presenter.cleanup();
		System.exit(0);
	}
	
	private static Node mountGraph(){
		SystemMonter monter  = new BaseMonter("resources\\injectFiles\\mainInject.txt");
		ArrayList<String> modulesNamesList = new ArrayList<>();
		return monter.mount(modulesNamesList);
	}
	
	private static void mainLoop(Node currentNode){
		Presenter.initViewModel();
		/*
		 * this trick lets switch control in just one code line and smoothly execute the logic
		 * of a freshly selected Node instance
		 */
		
		while (currentNode != null){
			logger.log(Level.INFO, "Current node: " + currentNode.getNodeName());
			currentNode = currentNode.nodeLoop();
		}
	}
	
	private static void checkIfViewReady(){
		//check if view layer is already set up
		while(true){
			try{
				Socket waiter = new Socket("localhost",2468);
				waiter.close();
				break;
			}
			catch(Exception e){
				logger.log(Level.INFO, "one more trial");
			}
		}
		logger.log(Level.INFO, "Connected with the view layer");
	}
}
