
// Linear Search Algorithms.
int linear_search(int a[], int item, int size){ // Normal version
  for(int i=0; i<size; i++){
    if(item == a[i]){
      return i;
    }
  }
  return -1; //returning -1 if key is not found
}

int rec_linear_search(int a[], int item , int size){ // Recursive approach
  if(size==1){
    return -1; //if key is not found
  } else if (item == a[size-1]){
    return size-1;
  } else{
    return rec_linear_search(a,item,size-1);
  }
}

// BINARY SEARCH ALGORITHMS
// NOTE: The Input Array for this approach must be sorted.
int binary_search(int array[], int s, int e, int item){ // Normal approach
  int mid = (e + s) / 2;
  if(item == array[mid]){
    return mid;
  } else if(item == array[s]){
    return s;
  } else if(item == array[e]){
    return e;
  } else{
    while(s <= e){
      if(item == array[mid]){
        return mid;
        break;
      } else if (item == array[s]){
        return s;
      } else if(item == array[e]){
        return e;
      } else if(item < array[mid]){
        mid = (s + e) / 2;
        e = mid - 1;
      } else if(item > array[mid]){
        mid = (s + e) / 2;
        s = mid + 1;
      } else{
        continue;
      }
    }
  }
  return -1;//returning -1 if key not found
}

int recursive_binary_search (int array[], int s, int e, int item){ // Recursive Method
  int mid = (e + s) / 2;
  if(s > e){
    return -1;
  }
  if(item == array[mid]){
    return mid;
  } else if(item == array[s]){
    return s;
  } else if(item == array[e]){
    return e;
  } else if (item < array[mid]){
    return recursive_binary_search(array , s, mid-1, item);
  } else if (item > array[mid]){
    return recursive_binary_search(array , mid+1, e, item);
  } else {
    return -1;
  }
}


