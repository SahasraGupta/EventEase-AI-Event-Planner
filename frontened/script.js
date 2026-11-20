async function generateRecommendations() {

    const userQuery = document.getElementById("userQuery").value.trim();
    const recommendations = document.getElementById("recommendations");
    const button = document.getElementById("generateBtn");

    if (!userQuery) {
        alert("Please enter your event requirements.");
        return;
    }

    const sections = {
        event_overview: "eventOverview",
        venue_recommendations: "venueRecommendations",
        food_recommendations: "foodRecommendations",
        decoration_recommendations: "decorationRecommendations",
        additional_recommendations: "otherRecommendations",
        budget_breakdown: "budgetBreakdown",
        information_sources: "recommendationSources"
    };

    // Create a safe HTML element with text
    function createTextElement(tag, text, className = "") {
        const element = document.createElement(tag);
        element.textContent = text || "Not available";

        if (className) {
            element.className = className;
        }

        return element;
    }

    // Display individual venue cards
    function displayVenueCards(venues, container) {

        container.innerHTML = "";

        if (!Array.isArray(venues) || venues.length === 0) {
            container.textContent = "No venue recommendations available.";
            return;
        }

        venues.forEach(venue => {

            const card = document.createElement("div");
            card.className = "venue-card";

            // Venue image
            if (venue.image_url) {

                const image = document.createElement("img");
                image.className = "venue-image";
                image.src = venue.image_url;
                image.alt = venue.name || "Venue image";
                image.loading = "lazy";

                image.onerror = () => image.remove();

                card.appendChild(image);
            }

            const details = document.createElement("div");
            details.className = "venue-details";

            // Venue name
            details.appendChild(
                createTextElement("h3", venue.name)
            );

            // Rating
            if (venue.rating) {
                details.appendChild(
                    createTextElement("p", "Rating: " + venue.rating)
                );
            }

            // Address
            details.appendChild(
                createTextElement("p", "Address: " + (venue.address || "Not available"))
            );

            // Capacity
            details.appendChild(
                createTextElement("p", "Capacity: " + (venue.capacity || "Not available"))
            );

            // Facilities
            const facilities = Array.isArray(venue.facilities)
                ? venue.facilities.join(", ")
                : "";

            details.appendChild(
                createTextElement("p", "Facilities: " + (facilities || "Not available"))
            );

            // Price
            details.appendChild(
                createTextElement("p", "Price: " + (venue.price || "Not available"))
            );

            // Source URL
            if (
                venue.source_url &&
                ["http:", "https:"].includes(new URL(venue.source_url).protocol)
            ) {
                const link = document.createElement("a");

                link.href = venue.source_url;
                link.textContent = "View Original Venue Website ↗";
                link.target = "_blank";
                link.rel = "noopener noreferrer";
                link.className = "venue-link";

                details.appendChild(link);
            } else {
                details.appendChild(
                    createTextElement("p", "Source link: Not available")
                );
            }

            card.appendChild(details);
            container.appendChild(card);
        });
    }

    try {

        button.disabled = true;
        button.innerText = "Generating...";

        Object.values(sections).forEach(id => {

            document
                .getElementById(id)
                .querySelector(".result-content")
                .innerText = "Generating recommendations...";

        });

        const response = await fetch("http://127.0.0.1:8000/event/requirements", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_query: userQuery
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }

        // Display all recommendations
        Object.entries(sections).forEach(([field, id]) => {

            const content = document
                .getElementById(id)
                .querySelector(".result-content");

            if (field === "venue_recommendations") {

                displayVenueCards(data[field], content);

            } else {

                content.innerText = data[field] || "No information available.";

            }

        });

    } catch (error) {

        recommendations.querySelectorAll(".result-content").forEach(content => {
            content.innerText = "Error: " + error.message;
        });

    } finally {

        button.disabled = false;
        button.innerText = "Generate Recommendations";

    }
}