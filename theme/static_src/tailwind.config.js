/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        "../templates/**/*.html",
        "../../templates/**/*.html",
        "../../**/templates/**/*.html",
    ],

    plugins: [
        require("daisyui"),
    ],

    daisyui: {
        themes: [
            "corporate",
            "light",
            "dark",
        ],
    },
}