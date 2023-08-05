
/**
 * Program to demonstrate examples that use the functions to calculate Semantic Similarity
 */

import py4j.GatewayServer;
public class Score{
	public static void main(String[] args){
		SimilarityScorer scorer = new SimilarityScorer();
		GatewayServer gatewayServer = new GatewayServer(scorer);
        gatewayServer.start();
	}
	
}
