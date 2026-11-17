
// ----------------------------------
// API CONFIGURATION
// ----------------------------------

const API_BASE = "http://127.0.0.1:8000";

const SEARCH_API = `${API_BASE}/ingredients/search`;
const RECOMMEND_API = `${API_BASE}/recipes/recommend`;


// Declaring Variables
let currentPage = 1;
let pageSize = 10;
let totalPages = 0;
let totalRecipes = 0;

// ----------------------------------
// DOM ELEMENTS
// ----------------------------------

const searchInput = document.getElementById("ingredientSearch");
const searchResults = document.getElementById("searchResults");
const selectedContainer = document.getElementById("selectedIngredients");
const recommendBtn = document.getElementById("recommendBtn");
const recipeResults = document.getElementById("recipeResults");
const recipeCount = document.getElementById("recipeCount");
const clearSearch = document.getElementById("clearSearch");
const pagination = document.getElementById("pagination");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const pageNumbers = document.getElementById("pageNumbers");
// ----------------------------------
// STATE
// ----------------------------------

// Store selected ingredients using their database IDs.

let selectedIngredients = new Map();

let debounceTimer;


// ----------------------------------
// 1. SEARCH INGREDIENTS
// ----------------------------------

searchInput.addEventListener("input", () => {

    clearTimeout(debounceTimer);

    const query = searchInput.value.trim();

    if (query.length < 2) {
        searchResults.innerHTML = "";
        return;
    }

    debounceTimer = setTimeout(() => {
        searchIngredients(query);
    }, 300);

});


async function searchIngredients(query) {

    try {

        searchResults.innerHTML = "<p>Searching...</p>";

        const response = await fetch(
            `${SEARCH_API}?q=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        console.log("API Response:", data);

        displaySearchResults(data.results);

    } catch (error) {

        console.error("Search Error:", error);

        searchResults.innerHTML =
            "<p>Unable to search ingredients.</p>";

    }

}


// ----------------------------------
// 2. DISPLAY SEARCH RESULTS
// ----------------------------------

function displaySearchResults(ingredients) {

    searchResults.innerHTML = "";

    if (ingredients.length === 0) {
        searchResults.innerHTML =
            "<p>No matching ingredients found.</p>";
        return;
    }

    ingredients.forEach(ingredient => {

        // Don't show ingredients already selected.

        if (selectedIngredients.has(ingredient.ingredient_id)) {
            return;
        }

        const item = document.createElement("div");
        item.className = "ingredient-option";

        const name = document.createElement("span");
        name.textContent = ingredient.canonical_name;

        const button = document.createElement("button");
        button.textContent = "+ Add";

        button.addEventListener("click", () => {
            addIngredient(ingredient);
        });

        item.appendChild(name);
        item.appendChild(button);

        searchResults.appendChild(item);

    });

}


// ----------------------------------
// 3. ADD INGREDIENT
// ----------------------------------

function addIngredient(ingredient) {

    const id = ingredient.ingredient_id;

    if (selectedIngredients.has(id)) {
        return;
    }

    selectedIngredients.set(id, ingredient);

    displaySelectedIngredients();

    // Refresh search results to remove selected item.

    displaySearchResultsFromCurrentQuery();

}


// ----------------------------------
// 4. DISPLAY SELECTED INGREDIENTS
// ----------------------------------

function displaySelectedIngredients() {

    selectedContainer.innerHTML = "";

    if (selectedIngredients.size === 0) {

        selectedContainer.innerHTML =
            '<p class="empty-message">No ingredients selected yet.</p>';

    }

    selectedIngredients.forEach((ingredient, id) => {

        const chip = document.createElement("div");
        chip.className = "ingredient-chip";

        const name = document.createElement("span");
        name.textContent = ingredient.canonical_name;

        const removeButton = document.createElement("button");
        removeButton.className = "remove-chip";
        removeButton.textContent = "×";

        removeButton.addEventListener("click", () => {
            removeIngredient(id);
        });

        chip.appendChild(name);
        chip.appendChild(removeButton);

        selectedContainer.appendChild(chip);

    });

    // Enable recommendation only if at least one ingredient exists.

    recommendBtn.disabled = selectedIngredients.size === 0;

}


// ----------------------------------
// 5. REMOVE INGREDIENT
// ----------------------------------

function removeIngredient(id) {

    selectedIngredients.delete(id);

    displaySelectedIngredients();

    displaySearchResultsFromCurrentQuery();

}


// ----------------------------------
// 6. REFRESH SEARCH RESULTS
// ----------------------------------

function displaySearchResultsFromCurrentQuery() {

    const query = searchInput.value.trim();

    if (query.length >= 2) {
        searchIngredients(query);
    }

}


// ----------------------------------
// 7. CLEAR SEARCH
// ----------------------------------

clearSearch.addEventListener("click", () => {

    searchInput.value = "";
    searchResults.innerHTML = "";

});


// ----------------------------------
// 8. GET RECIPE RECOMMENDATIONS
// ----------------------------------
recommendBtn.addEventListener("click", async () => {

    if (selectedIngredients.size === 0) {
        return;
    }

    currentPage = 1;

    await fetchRecommendations(currentPage);

});

async function fetchRecommendations(page) {

    recommendBtn.disabled = true;
    prevBtn.disabled = true;
    nextBtn.disabled = true;

    try {

        recommendBtn.disabled = true;
        recommendBtn.textContent = "Finding Recipes...";

        recipeResults.innerHTML =
            "<p>Finding recipes for you...</p>";

        const ingredientIds = Array.from(
            selectedIngredients.keys()
        );

        const response = await fetch(
            `${RECOMMEND_API}?page=${page}&page_size=${pageSize}`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    ingredient_ids: ingredientIds
                })
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        console.log("Recommendation Response:", data);

        // Update pagination buttons
        updatePagination(data);

        // Display recipes for the current page
        displayRecipes(data.results);


    } catch (error) {

        console.error("Recommendation Error:", error);

        recipeResults.innerHTML =
            "<p>Unable to fetch recommendations. Please try again.</p>";

    } finally {

        recommendBtn.disabled = selectedIngredients.size === 0;
        recommendBtn.textContent = "Find Recipes";

    }

}

prevBtn.addEventListener("click", () => {

    if (currentPage > 1) {
        fetchRecommendations(currentPage - 1);
    }

});

nextBtn.addEventListener("click", () => {

    if (currentPage < totalPages) {
        fetchRecommendations(currentPage + 1);
    }

});



// ----------------------------------
// 9. DISPLAY RECOMMENDED RECIPES
// ----------------------------------


function displayRecipes(recipes) {

    recipeResults.innerHTML = "";

    recipeCount.textContent =
        `${totalRecipes} recipes found`;

    if (recipes.length === 0) {

        recipeResults.innerHTML =
            "<p>No recipes found for these ingredients.</p>";

        return;
    }

    recipes.forEach(recipe => {

        const card = document.createElement("div");
        card.className = "recipe-card";

        // Recipe name
        const title = document.createElement("h3");
        title.textContent = recipe.recipe_name;

        // Match percentage
        const percentage = document.createElement("p");
        percentage.className = "match";
        percentage.textContent =
            `${recipe.match_percentage}% Match`;

        // Matched ingredients
        const matched = document.createElement("p");
        matched.textContent =
            `Available ingredients: ${
                recipe.matched_ingredients.join(", ") || "None"
            }`;

        // Missing ingredients
        const missing = document.createElement("p");
        missing.textContent =
            `Missing ingredients: ${
                recipe.missing_ingredients.join(", ") || "None"
            }`;

        // Ingredient statistics
        const stats = document.createElement("p");
        stats.textContent =
            `${recipe.matched_count} / ${recipe.total_ingredients} ingredients available`;

        // Can make now status
        const status = document.createElement("p");

        if (recipe.can_make_now) {

            status.textContent = "You can make this recipe now!";
            status.style.color = "green";

        } else {

            status.textContent =
                `You need ${recipe.missing_count} more ingredients`;

            status.style.color = "#d97706";

        }

        // Append everything to the card
        card.appendChild(title);
        card.appendChild(percentage);
        card.appendChild(stats);
        card.appendChild(matched);
        card.appendChild(missing);
        card.appendChild(status);

        recipeResults.appendChild(card);

    });

}


// UPDATE PAGINATION
function updatePagination(data) {

    // Update pagination state
    currentPage = data.page;
    totalPages = data.total_pages;
    totalRecipes = data.total_recipes;

    // Display current page information
    pageInfo.textContent =
        `Page ${currentPage} of ${totalPages}`;

    // Disable Previous button on first page
    prevBtn.disabled = currentPage <= 1;

    // Disable Next button on last page
    nextBtn.disabled = currentPage >= totalPages;

}