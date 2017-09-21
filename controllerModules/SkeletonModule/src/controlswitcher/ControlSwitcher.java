package controlswitcher;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.net.Socket;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;

import py4jmediator.Presenter;
import controlnode.Node;
import model.DependenciesRepresenter;
import monter.BaseMonter;
import monter.SystemMonter;

public class ControlSwitcher {

	private static Presenter presenter;
	
	public static void main(String[] args)throws Exception{
		presenter = Presenter.getInstance(); 
		checkIfViewReady();
		Node currentNode = mountGraph(args);
		mainLoop(currentNode);
		cleanup();
	}	

	
	private static void cleanup(){
		Presenter.cleanup();
		System.exit(0);
	}
	
	private static Node mountGraph(String[] args){

		/*
		 * possible args values:
		 * -noide
		 */
		
		SystemMonter monter  = new BaseMonter("resources\\injectFiles\\mainInject.txt",args);
		ArrayList<String> modulesNamesList = new ArrayList<>();
		return monter.mount(modulesNamesList);
	}
	
	private static void mainLoop(Node currentNode){
		presenter.initViewModel();
		/*
		 * this trick lets switch control in just one code line and smoothly execute the logic
		 * of a freshly selected Node instance
		 */
		
		while (currentNode != null){
			System.out.println("Current node: " + currentNode.getNodeName());
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
				System.out.println("One more trial");
			}
		}
		System.out.println("Connected, view layer active");			
	}
}
