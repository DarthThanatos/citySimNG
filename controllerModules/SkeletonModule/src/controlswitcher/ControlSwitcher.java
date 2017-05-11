package controlswitcher;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.net.Socket;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;

import controlnode.Node;
import model.DependenciesRepresenter;
import monter.BaseMonter;
import monter.SystemMonter;

public class ControlSwitcher {

		public static void main(String[] args)throws Exception{	 	
			/*
			 * possible args values:
			 * -noide
			 */
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
			
			SystemMonter monter  = new BaseMonter("resources\\injectFiles\\mainInject.txt",args);
			ArrayList<String> modulesNamesList = new ArrayList<>();
			Node currentNode = monter.mount(modulesNamesList);
			while (currentNode != null){
				currentNode = currentNode.nodeLoop(); 
				/*
				 * ^ this trick lets switch control in just one code line and smoothly execute the logic
				 * of a freshly selected Node instance
				 */
			}
		}
}
