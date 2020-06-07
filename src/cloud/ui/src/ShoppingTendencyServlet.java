import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import javax.annotation.Resource;
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
import java.sql.ResultSet;
import java.util.ArrayList;

@WebServlet(name = "shopping-tendency", urlPatterns = "/api/shopping-tendency")
public class ShoppingTendencyServlet extends HttpServlet {
	@Resource(name = "jdbc/smart_shopping_cart")
	private DataSource dataSource;
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setContentType("application/json");
		PrintWriter out = response.getWriter();

		try {
			Connection dbcon = dataSource.getConnection();

			String query = "select item, count(*) coun from shopping_history group by item order by coun asc;";

			PreparedStatement statement = dbcon.prepareStatement(query);
			ResultSet rs = statement.executeQuery();
			JsonArray jsonArray = new JsonArray();

			ArrayList<String> item = new ArrayList<String>();
			ArrayList<Integer> coun = new ArrayList<Integer>();
			int total = 0;

			while (rs.next()) {
				item.add(rs.getString("item"));
				int item_count = Integer.parseInt(rs.getString("coun"));
				coun.add(item_count);
				total += item_count;
			}

			for(int i = 0; i < item.size(); i++) {
				JsonObject jsonObject = new JsonObject();
				jsonObject.addProperty("item", item.get(i));
				double percentage = coun.get(i) * 1.0 / total;
				jsonObject.addProperty("percentage", percentage);
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
