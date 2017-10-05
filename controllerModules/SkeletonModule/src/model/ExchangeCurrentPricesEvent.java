package model;

import java.util.HashMap;

public class ExchangeCurrentPricesEvent {

    private HashMap<String, Integer> currentPrices;

    public ExchangeCurrentPricesEvent(HashMap<String, Integer> currentPrices){
        this.currentPrices = currentPrices;
    }

    public HashMap<String, Integer> getCurrentPrices(){
        return currentPrices;
    }
}
