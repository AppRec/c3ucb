/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package c3ucb;
import java.util.Hashtable;
import Jama.Matrix;

/**
 *
 * @author wudi
 */
public class C3UCB {
    private int k;
    private int pool_size;
    private boolean usingUser; //decide whether to use user feature or not
    private Parameters params;
    private double lamb;
    private double delta;
    private double gama;
    private double R;
    private String[] app_list;
    private Matrix af; //matrix consisting of Apps feature
    private Matrix[] xf_hist; // matrix consisting of history x features
    
    public C3UCB(Setting s){
        this.k = s.sizeOfAction;
        this.pool_size = s.numOfApps;
        this.usingUser = s.userInfo;
        this.params = new Parameters(s.d, s.initial_beta, s.lamb);
        this.delta = s.delta;
        this.gama = s.gama;
        this.lamb = s.lamb;
        this.R = s.R;
        this.af = getAppFeature();
        this.app_list = getAppID();
        this.xf_hist = new Matrix[1];
        this.xf_hist[0] = new Matrix(1,s.d);
    }
    
    public String[] recommendApps(String uid){ //The interface must give a user id to C3UCB
        if(usingUser) return recommend_withUser(uid);
        else return recommend_noUser();
    }
    
    public void updateAppPool(){
        af = getAppFeature();
        app_list = getAppID(); 
    }

    private String[] recommend_withUser(String uid) {
        Matrix uf = getUserFeature(uid);
        Matrix xf = computeOuterProduct(af, uf);
        Hashtable UCBs = calculateUCB(xf);
        int[] app_idx = getTopKApps();
        String[] action = new String[k];
        for(int i=0; i<app_idx.length; i++) { action[i] = app_list[app_idx[i]]; }
        addToHistory(xf, app_idx);
        return action;
    }
    
    private String[] recommend_noUser() {
        Matrix xf = af;
        Hashtable UCBs = calculateUCB(xf);
        int[] app_idx = getTopKApps();
        String[] action = new String[k];
        for(int i=0; i<app_idx.length; i++) { action[i] = app_list[app_idx[i]]; }
        addToHistory(xf, app_idx);
        return action;
    }
    
    private String[] getAppID(){
        return new String[]{"abc","cvd","qwe"};
    }
    
    private Matrix getAppFeature(){
        double[][] tmp = {{1,1,1},{2,2,2}};
        Matrix af = new Matrix(tmp);
        return af;
    }
    
    private Matrix getUserFeature(String uid){
        Matrix uf = new Matrix(new double[]{1,1,1},1);
        return uf;
    }
    
    private Matrix computeOuterProduct(Matrix af, Matrix uf){
        Matrix xf = new Matrix(new double[]{123},1);
        return xf;
    }
    
    //consider to use Treemap
    private Hashtable calculateUCB(Matrix xf){ 
        Hashtable UCBs = new Hashtable(pool_size); 
        return UCBs;
    }
    
    private int[] getTopKApps(){
        int[] idx = {1,2,3};
        return idx;
    }
    
    private void addToHistory(Matrix xf, int[] idx){
        Matrix[] new_xf_hist = new Matrix[xf_hist.length+1];
        new_xf_hist[new_xf_hist.length-1] = xf.getMatrix(idx,0,xf.getColumnDimension()-1);
        this.xf_hist = new_xf_hist;
    }
    
    public void updateModel(int[][] feedback){ 
    // supose feedback with 2-dimension, the row is the index of recommendation, the column is the feedback to each app.
    // cliked = 1, download = 2, ignore = 0(all 0s will be treated as 'dislike')
        double[][] feedback_d = new double[feedback.length][feedback[0].length];
        for(int i=0; i<feedback.length; i++){
            for(int j=0; j<feedback[0].length; j++){
                feedback_d[i][j] = feedback[i][j];
            }
        }
        for(int i=0; i<feedback_d.length; i++){
            Matrix w = new Matrix(feedback_d[i],1);
            w = w.transpose();
            int num_w = w.getRowDimension();
            Matrix xfs = xf_hist[i]; //a set of x feature of one action
            int num_x = xfs.getRowDimension();
            int dim = xfs.getColumnDimension();
            for(int j=0; j<num_x; j++){
                Matrix xf = xfs.getMatrix(j,j,0,dim-1);
                params.V = params.V.plus(xf.transpose().times(xf).times(Math.pow(gama,2)));
                xf = xf.times(gama);
                xfs.setMatrix(j,j,0,dim-1,xf);
            }
            Matrix newX = new Matrix(params.X.getRowDimension()+num_x, params.X.getColumnDimension());
            newX.setMatrix(0,params.X.getRowDimension()-1, 0, params.X.getColumnDimension()-1, params.X);
            newX.setMatrix(params.X.getRowDimension(), newX.getRowDimension()-1, 0, params.X.getColumnDimension()-1, xfs);
            params.X = newX;
            
            w = w.times(gama);
            Matrix newY = new Matrix(params.Y.getRowDimension()+num_w,1);
            newY.setMatrix(0, params.Y.getRowDimension()-1, 0, 0, params.Y);
            newY.setMatrix(params.Y.getRowDimension(), newY.getRowDimension()-1, 0, 0, w);
            params.Y = newY;
            
            Matrix I = Matrix.identity(dim, dim).times(lamb);
            /*params.theta = ;
            params.beta = ;*/
        }
    }
    
    public static void main(String[] args) {
        // TODO code application logic here
    }

    
    
}
