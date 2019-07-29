function showFiles(input, filenames, filesizes) {

  var input = document.getElementById(input)
  var filenames = document.getElementById(filenames)
  var filesizes = document.getElementById(filesizes)

  filenames.innerHTML = ''
  filesizes.innerHTML = ''

  for (var x = 0; x < input.files.length; x++) {

    var filename_div = document.createElement('div')
    filename_div.classList.add('text-truncate')
    filename_div.innerHTML = input.files[x].name
    filenames.append(filename_div)

    var filesize_div = document.createElement('li')
    filesize_div.classList.add('text-truncate')
    filesize_div.innerHTML = formatBytes(input.files[x].size)
    filesizes.append(filesize_div)
  }
}


function formatBytes(bytes) {

  if (bytes <= 1024) {
    return (bytes / 1024).toFixed(2) + ' KB'
  }

  else {
    var i = Math.floor(Math.log(bytes) / Math.log(1024)),
    sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    return (bytes / Math.pow(1024, i)).toFixed(2) + ' ' + sizes[i]
  }
}