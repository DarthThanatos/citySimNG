package controlswitcher;

import controlnode.Node;
import monter.FileMonter;
import monter.SystemMonter;

public class ControlSwitcher {

		public static void main(String[] args)throws Exception{			
			SystemMonter monter  = new FileMonter("inject.txt");
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
