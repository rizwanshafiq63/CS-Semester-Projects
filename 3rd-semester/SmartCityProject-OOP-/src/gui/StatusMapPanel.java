// gui/StatusMapPanel.java
package gui;

import models.CityResource;

import javax.swing.*;
import java.awt.*;
import java.util.List;
import java.util.ArrayList;

public class StatusMapPanel extends JPanel {
    private List<CityResource> resources = new ArrayList<>();

    public void setResources(List<CityResource> resources) {
        this.resources = resources;
        repaint(); // redraw panel when data updates
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        int x = 20, y = 30;
        int width = 100, height = 40;
        int gap = 10;

        for (CityResource r : resources) {
            // Set color by status
            switch (r.getStatus().toLowerCase()) {
                case "active":
                    g.setColor(Color.GREEN);
                    break;
                case "maintenance":
                    g.setColor(Color.ORANGE);
                    break;
                case "offline":
                    g.setColor(Color.RED);
                    break;
                default:
                    g.setColor(Color.GRAY);
            }

            g.fillRect(x, y, width, height);
            g.setColor(Color.BLACK);
            g.drawRect(x, y, width, height);
            g.drawString(r.getResourceID(), x + 5, y + 25);

            y += height + gap;
            if (y > getHeight() - height) {
                y = 30;
                x += width + gap;
            }
        }
    }
}



