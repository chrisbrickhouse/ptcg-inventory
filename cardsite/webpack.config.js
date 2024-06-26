const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,
  entry: {
	  main: "./assets/js/index.js",
	  decklist: "./assets/js/decklist_loader.js"
  },
  output: {
    path: path.resolve(__dirname, "assets/webpack_bundles/"),
    publicPath: "auto", // necessary for CDNs/S3/blob storages
    filename: "[name]-[contenthash].js",
    library: "ptcglobal",
  },
  plugins: [
    new BundleTracker({ path: __dirname, filename: "webpack-stats.json" }),
  ],
};
