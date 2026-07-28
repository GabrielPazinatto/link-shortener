<?php
$api_url = "https://link-shortener-backend-nu.vercel.app/api";

$short_url = trim($_SERVER['REQUEST_URI'], '/');

if (!empty($short_url)) {
    $redirect_url = "$api_url/$short_url";
    header("Location: $redirect_url");
    exit();
} else {
    echo "<h1>Welcome to Shortify!</h1><p>Please provide a valid short link.</p>";
}
?>
