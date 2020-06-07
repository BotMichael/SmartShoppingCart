import com.google.gson.JsonObject;

import javax.annotation.Resource;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.sql.DataSource;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;


// Declaring a WebServlet called StarsServlet, which maps to url "/api/stars"
@WebServlet(name = "AddactionServlet", urlPatterns = "/api/addaction")
public class AddActionServlet extends HttpServlet {
    @Resource(name = "jdbc/smart_shopping_cart")
    private DataSource dataSource;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String action = request.getParameter("action");
        try {
            Connection dbcon = dataSource.getConnection();
            PrintWriter out = response.getWriter();
            if (action != null) {
                if (action.equals("add_user")) {
                    String phone = request.getParameter("phone");
                    String password = request.getParameter("password");

                    System.out.println(phone + " " + password);
                    String sql = "INSERT INTO user values (?, ?)";
                    PreparedStatement preparedStatement = dbcon.prepareStatement(sql);
                    preparedStatement.setString(1, phone);
                    preparedStatement.setString(2, password);
                    int value = preparedStatement.executeUpdate();
                    JsonObject jsonObject = new JsonObject();
                    if(value > 0){
                        jsonObject.addProperty("status", "success");
                        jsonObject.addProperty("phone", phone);
                    }
                    else{
                        jsonObject.addProperty("status", "fail");
                    }
                    out.write(jsonObject.toString());
                }
                if (action.equals("add_item")) {
                    String item = request.getParameter("item").toLowerCase();
                    String region = request.getParameter("region").toUpperCase();
                    Float price = Float.parseFloat(request.getParameter("price"));

                    String sql = "INSERT INTO item values (?, ?, ?)";
                    PreparedStatement preparedStatement = dbcon.prepareStatement(sql);
                    preparedStatement.setString(1, item);
                    preparedStatement.setString(2, region);
                    preparedStatement.setFloat(3, price);
                    int value = preparedStatement.executeUpdate();
                    JsonObject jsonObject = new JsonObject();
                    if(value > 0){
                        jsonObject.addProperty("status", "success");
                        jsonObject.addProperty("item", item);
                        jsonObject.addProperty("region", region);
                        jsonObject.addProperty("price", price);
                    }
                    else{
                        jsonObject.addProperty("status", "fail");
                    }
                    out.write(jsonObject.toString());
                }
                out.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
