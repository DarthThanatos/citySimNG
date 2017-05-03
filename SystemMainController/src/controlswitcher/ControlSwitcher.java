package controlswitcher;

import java.io.IOException;
import java.lang.reflect.Constructor;
import java.net.URL;
import java.net.URLClassLoader;

import controlnode.Node;
import model.DependenciesRepresenter;
import monter.FileMonter;
import monter.SystemMonter;

public class ControlSwitcher {

		public static void main(String[] args)throws Exception{	 	
			/*
			 * possible args values:
			 * -noide
			 */
			SystemMonter monter  = new FileMonter("inject.txt",args);
			Node currentNode = monter.mount();
			while (currentNode != null){
				currentNode = currentNode.nodeLoop(); 
				/*
				 * ^ this trick lets switch control in just one code line and smoothly execute the logic
				 * of a freshly selected Node instance
				 */
			}
		}
}
