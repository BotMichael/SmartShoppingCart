import com.google.gson.JsonObject;
import javax.annotation.Resource;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.sql.DataSource;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.*;


@WebServlet(name = "LoginServlet", urlPatterns = "/api/login")
public class LoginServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        JsonObject responseJsonObject = new JsonObject();

        String username = request.getParameter("username");
        String password = request.getParameter("password");
        PrintWriter out = response.getWriter();
        try {
            if(username.equalsIgnoreCase("admin") && password.equalsIgnoreCase("admin")){
                HttpSession session = request.getSession();
                session.setAttribute("user", "admin");
                session.setAttribute("accessBoolean", true);
                responseJsonObject.addProperty("status", "success");
                responseJsonObject.addProperty("message", "Success.");
            }
            else{
                responseJsonObject.addProperty("status", "fail");
                responseJsonObject.addProperty("message", "Incorrect username or password.");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        out.write(responseJsonObject.toString());
        out.close();
    }
}

