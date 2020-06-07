import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import javax.annotation.Resource;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.sql.DataSource;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

@WebServlet(name = "visits", urlPatterns = "/api/visits")
public class VisitsServlet extends HttpServlet {
	@Resource(name = "jdbc/smart_shopping_cart")
	private DataSource dataSource;
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setContentType("application/json");
		PrintWriter out = response.getWriter();

		try {
			Connection dbcon = dataSource.getConnection();

			String query = "select date_format(time, '%Y-%m-%d') dat, count(*) coun " +
							"from shopping_history " +
							"group by date_format(time, '%Y-%m-%d') " +
							"order by dat;";

			PreparedStatement statement = dbcon.prepareStatement(query);
			ResultSet rs = statement.executeQuery();
			JsonArray jsonArray = new JsonArray();

			while (rs.next()) {
				String date = rs.getString("dat");
				String visits = rs.getString("coun");

				JsonObject jsonObject = new JsonObject();
				jsonObject.addProperty("date", date);
				jsonObject.addProperty("visits", visits);
				jsonArray.add(jsonObject);
			}
            out.write(jsonArray.toString());
            response.setStatus(200);
			rs.close();
			statement.close();
			dbcon.close();
		} catch (Exception e) {
			JsonObject jsonObject = new JsonObject();
			jsonObject.addProperty("errorMessage", e.getMessage());
			out.write(jsonObject.toString());
			response.setStatus(500);
		}
		out.close();
	}
}
