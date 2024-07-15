const fs = require('fs');
const path = require('path');
const { optimize } = require('svgo');

// Configure SVGO options with built-in plugins
const svgoConfig = {
  plugins: [
    'removeDoctype',
    'removeXMLProcInst',
    'removeComments',
    'removeMetadata',
    'removeEditorsNSData',
    'cleanupAttrs',
    'inlineStyles',
    'minifyStyles',
    'convertStyleToAttrs',
    'removeRasterImages',
    'mergePaths',
    'convertShapeToPath',
    'sortAttrs',
    'removeDimensions',
    {
      name: 'removeViewBox',
      active: false
    }
  ]
};

// Directory containing SVG files
const svgDir = 'output'; // Input directory
const outputDir = 'svg'; // Output directory

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.readdir(svgDir, (err, files) => {
  if (err) throw err;

  files.filter(file => file.endsWith('.svg')).forEach(file => {
    const filePath = path.join(svgDir, file);
    const outputFilePath = path.join(outputDir, file);

    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) throw err;

      const result = optimize(data, { path: filePath, plugins: svgoConfig.plugins });
      fs.writeFile(outputFilePath, result.data, err => {
        if (err) throw err;
        console.log(`Processed ${file}`);
      });
    });
  });
});
